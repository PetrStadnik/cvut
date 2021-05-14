#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>

#include <assert.h>

#include <termios.h>
#include <unistd.h> // for STDIN_FILENO

#include <pthread.h>

#include "prg_serial_nonblock.h"
#include "messages.h"
#include "event_queue.h"
#include "computation.h"
#include "utils.h"
#include "gui.h"
#include "xwin_sdl.h"

#define SERIAL_READ_TIMOUT_MS 500 //timeout for reading from serial port

#define SERIAL_PORT "/dev/ttyACM0"
// shared data structure
typedef struct
{
    bool quit;
    int fd; // serial port file descriptor
} data_t;

pthread_mutex_t mtx;
pthread_cond_t cond;

void *input_thread(void *);
void *serial_rx_thread(void *); // serial receive buffer

bool send_message(data_t *data, message *msg);

// - main ---------------------------------------------------------------------
int main(int argc, char *argv[])
{
    data_t data = {.quit = false, .fd = -1};
    const char *serial = argc > 1 ? argv[1] : SERIAL_PORT;
    data.fd = serial_open(serial);

    if (data.fd == -1)
    {
        fprintf(stderr, "ERROR: Cannot open serial port %s\n", serial);
        exit(100);
    }

    enum
    {
        INPUT,
        SERIAL_RX,
        NUM_THREADS
    };
    const char *threads_names[] = {"Input", "Serial In"};

    void *(*thr_functions[])(void *) = {input_thread, serial_rx_thread};

    pthread_t threads[NUM_THREADS];
    pthread_mutex_init(&mtx, NULL); // initialize mutex with default attributes
    pthread_cond_init(&cond, NULL); // initialize mutex with default attributes

    call_termios(0);

    for (int i = 0; i < NUM_THREADS; ++i)
    {
        int r = pthread_create(&threads[i], NULL, thr_functions[i], &data);
        fprintf(stderr, "INFO: Create thread '%s' %s\n", threads_names[i], (r == 0 ? "OK" : "FAIL"));
    }

    // example of local  messaging
    message msg;

    bool quit = false;

    computation_init();
    gui_init();
    while (!quit)
    {
        event ev = queue_pop();
        if (ev.source == EV_KEYBOARD)
        {
            msg.type = MSG_NBR;
            // handle keyboard events
            switch (ev.type)
            {
            case EV_GET_VERSION:
            { // prepare packet for get version
                msg.type = MSG_GET_VERSION;
                fprintf(stderr, "INFO: Get version requested\n");
            }
            break;
            case EV_REFRESH:
            {
                info("Refresh");
                gui_refresh();
            }
            break;
            case EV_CLEAR_BUFFER:
            {
                info("Clear buffer");
                clear_buffer();
            }
            break;
            case EV_COMPUTE_CPU:
            {
                info("CPU compute");
                juli_comp();
                gui_refresh();
                info("CPU computed");
            }
            break;
            case EV_SET_COMPUTE:
            {
                info(set_compute(&msg) ? "set compute" : "fail set compute");
            }
            break;
            case EV_COMPUTE:
            {
                enable_comp();
                info(compute(&msg) ? "compute" : "fail compute");
            }
            break;
            case EV_ABORT:
            {
                msg.type = MSG_ABORT;
                abort_comp();
                fprintf(stderr, "INFO: Abort from Nucleo requested\n");
            }
            break;
            case EV_RESET_CHUNK:
            {
                abort_comp();
                info("Reset cid");
                reset_cid();
            }
            break;
            case EV_ANIMATE:
            {
                info("Animate");
                animate();
                info("Animate done");
            }
            break;
            case EV_PHOTO:
            {
                info(save_image() ? "Image saved" : "Failed save image");
            }
            break;
            case EV_QUIT:
            {
                msg.type = MSG_ABORT;
                fprintf(stderr, "INFO: Abort from Nucleo requested\n");
                quit = true;
            }
            break;
            default:
                break;
            }
            if (msg.type != MSG_NBR)
            { // messge has been set
                if (!send_message(&data, &msg))
                {
                    fprintf(stderr, "ERROR: send_message() does not send all bytes of the message!\n");
                }
            }
        }
        else if (ev.source == EV_NUCLEO)
        { // handle nucleo events
            if (ev.type == EV_SERIAL)
            {
                message *msg = ev.data.msg;
                switch (msg->type)
                {
                case MSG_STARTUP:
                {
                    char str[STARTUP_MSG_LEN + 1];
                    for (int i = 0; i < STARTUP_MSG_LEN; ++i)
                    {
                        str[i] = msg->data.startup.message[i];
                    }
                    str[STARTUP_MSG_LEN] = '\0';
                    fprintf(stderr, "INFO: Nucleo restarted - '%s'\n", str);
                }
                break;
                case MSG_VERSION:
                    if (msg->data.version.patch > 0)
                    {
                        fprintf(stderr, "INFO: Nucleo firmware ver. %d.%d-p%d\n", msg->data.version.major, msg->data.version.minor, msg->data.version.patch);
                    }
                    else
                    {
                        fprintf(stderr, "INFO: Nucleo firmware ver. %d.%d\n", msg->data.version.major, msg->data.version.minor);
                    }
                    break;
                case MSG_ERROR:
                    fprintf(stderr, "WARN: Receive error from Nucleo\n");
                    break;
                case MSG_OK:
                    fprintf(stderr, "INFO: Receive ok from Nucleo\n");
                    break;
                case MSG_COMPUTE_DATA:
                    if (!is_abort())
                    {
                        update_data(&(msg->data.compute_data));
                    }
                    //fprintf(stderr, "Compute data cid: %d iter: %d x: %d y: %d \n", msg->data.compute_data.cid, msg->data.compute_data.iter, msg->data.compute_data.i_re, msg->data.compute_data.i_im );
                    break;
                case MSG_DONE:
                    gui_refresh();
                    if (is_done())
                    {
                        info("Computation done");
                    }
                    else
                    {
                        if (!is_abort())
                        {
                            info("Want next chunk");
                            event ev = {.source = EV_KEYBOARD, .type = EV_COMPUTE};
                            queue_push(ev);
                        }
                    }
                    break;
                case MSG_ABORT:
                    fprintf(stderr, "INFO: Abort from Nucleo\n");
                    abort_comp();
                    break;
                default:
                    break;
                }
                if (msg)
                {
                    free(msg);
                }
            }
            else if (ev.type == EV_QUIT)
            {
                quit = true;
            }
            else
            {
                // ignore all other events
            }
        }
    }                // end main quit
    queue_cleanup(); // cleanup all events and free allocated memory for messages.
    computation_cleanup();
    gui_cleanup();
    pthread_mutex_lock(&mtx);
    data.quit = true;
    pthread_mutex_unlock(&mtx);
    for (int i = 0; i < NUM_THREADS; ++i)
    {
        fprintf(stderr, "INFO: Call join to the thread %s\n", threads_names[i]);
        int r = pthread_join(threads[i], NULL);
        fprintf(stderr, "INFO: Joining the thread %s has been %s\n", threads_names[i], (r == 0 ? "OK" : "FAIL"));
    }
    pthread_mutex_lock(&mtx);
    serial_close(data.fd);
    pthread_mutex_unlock(&mtx);
    call_termios(1); // restore terminal settings
    return EXIT_SUCCESS;
}

// - function -----------------------------------------------------------------

void *input_thread(void *d)
{
    data_t *data = (data_t *)d;
    bool end = false;
    int c;
    event ev = {.source = EV_KEYBOARD};
    while (!end && (c = getchar()))
    {
        ev.type = EV_TYPE_NUM;
        switch (c)
        {
        case 'g': // get version
            ev.type = EV_GET_VERSION;
            break;
        case 'a': // abort
            ev.type = EV_ABORT;
            break;
        case 'm': // abort
            ev.type = EV_ANIMATE;
            break;
        case 's':
            ev.type = EV_SET_COMPUTE;
            break;
        case '1':
            ev.type = EV_COMPUTE;
            break;
        case 'q':
            end = true;
            break;
        case 'r':
            ev.type = EV_RESET_CHUNK;
            break;
        case 'l':
            ev.type = EV_CLEAR_BUFFER;
            break;
        case 'p':
            ev.type = EV_REFRESH;
            break;
        case 'c':
            ev.type = EV_COMPUTE_CPU;
            break;
        case 'i':
            ev.type = EV_PHOTO;
            break;
        default: // discard all other keys

            break;
        }
        if (ev.type != EV_TYPE_NUM)
        { // new event
            queue_push(ev);
        }
        pthread_mutex_lock(&mtx);
        end = end || data->quit; // check for quit
        pthread_mutex_unlock(&mtx);
    }
    ev.type = EV_QUIT;
    queue_push(ev);
    fprintf(stderr, "INFO: Exit input thead %p\n", (void *)pthread_self());
    return NULL;
}

// - function -----------------------------------------------------------------
void *serial_rx_thread(void *d)
{ // read bytes from the serial and puts the parsed message to the queue
    data_t *data = (data_t *)d;
    uint8_t msg_buf[sizeof(message)]; // maximal buffer for all possible messages defined in messages.h
    event ev = {.source = EV_NUCLEO, .type = EV_SERIAL, .data.msg = NULL};
    bool end = false;
    unsigned char c;
    int len = 0;
    int i = 0;
    while (serial_getc_timeout(data->fd, SERIAL_READ_TIMOUT_MS, &c) > 0)
    {
    }; // discard garbage

    while (!end)
    {
        int r = serial_getc_timeout(data->fd, SERIAL_READ_TIMOUT_MS, &c);
        if (r > 0)
        {
            if (i == 0)
            {
                len = 0;
                if (get_message_size(c, &len))
                {
                    msg_buf[i++] = c;
                }
                else
                {
                    fprintf(stderr, "ERROR: Unknown message type has been received 0x%x\n - '%c'\r", c, c);
                }
            }
            else
            {
                msg_buf[i++] = c;
            }

            if (len > 0 && len == i)
            {
                message *msg = my_alloc(sizeof(message));
                if (parse_message_buf(msg_buf, len, msg))
                {
                    event ev = {.type = EV_SERIAL};
                    ev.data.msg = msg;
                    queue_push(ev);
                }
                else
                {
                    fprintf(stderr, "ERROR: Cannot parse message type %d\n", msg_buf[0]);
                    free(msg);
                }
                i = 0;
                len = 0;
            }
        }
        else if (r == 0)
        {
        }
        else
        {
            fprintf(stderr, "ERROR: Cannot receive data from the serial port\r\n");
            end = true;
            pthread_mutex_lock(&mtx);
            data->quit = true;
            pthread_mutex_unlock(&mtx);
            event ev = {.type = EV_QUIT};
            queue_push(ev);
        }
        pthread_mutex_lock(&mtx);
        end = end || data->quit;
        pthread_mutex_unlock(&mtx);
    }
    ev.type = EV_QUIT;
    queue_push(ev);
    fprintf(stderr, "INFO: Exit serial_rx_thread %p\n", (void *)pthread_self());
    return NULL;
}

// - function -----------------------------------------------------------------
bool send_message(data_t *data, message *msg)
{
    bool ret = false;
    int size;
    int len;
    get_message_size(msg->type, &size);
    uint8_t msg_buf[sizeof(message)]; // maximal buffer for all possible messages defined in messages.h
    fill_message_buf(msg, msg_buf, sizeof(message), &len);
    if (write(data->fd, msg_buf, len) == len)
    {
        ret = true;
    }
    return ret;
}
