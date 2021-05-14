#include "computation.h"

static struct
{
    double c_re;
    double c_im;
    int n;

    double range_re_min;
    double range_re_max;
    double range_im_min;
    double range_im_max;

    int grid_w;
    int grid_h;

    int cur_x;
    int cur_y;

    double d_re;
    double d_im;

    int nbr_chunks;
    int cid;
    double chunk_re;
    double chunk_im;

    uint8_t chunk_n_re;
    uint8_t chunk_n_im;

    uint8_t *grid;
    bool computing;
    bool abort;
    bool done;
} comp = {
    .c_re = -0.4,
    .c_im = 0.6,

    .n = 60,

    .range_re_min = -1.6,
    .range_re_max = 1.6,
    .range_im_min = -1.1,
    .range_im_max = 1.1,

    .grid = NULL,
    .grid_w = 1200,
    .grid_h = 800,

    .chunk_n_re = 64,
    .chunk_n_im = 48,

    .computing = false,
    .abort = false,
    .done = false};

void computation_init(void)
{
    comp.grid = my_alloc(comp.grid_w * comp.grid_h);
    comp.d_re = (comp.range_re_max - comp.range_re_min) / (1. * comp.grid_w);
    comp.d_im = -(comp.range_im_max - comp.range_im_min) / (1. * comp.grid_h);
    comp.nbr_chunks = (comp.grid_w * comp.grid_h) / (comp.chunk_n_re * comp.chunk_n_im);
}
void computation_cleanup(void)
{
    if (comp.grid)
    {
        free(comp.grid);
    }
    comp.grid = NULL;
}

void get_grid_size(int *w, int *h)
{
    *w = comp.grid_w;
    *h = comp.grid_h;
}

bool is_computing(void) { return comp.computing; }
bool is_done(void) { return comp.done; }
bool is_abort(void) { return comp.abort; }

void abort_comp(void) { comp.abort = true; }
void enable_comp(void) { comp.abort = false; }

bool set_compute(message *msg)
{
    my_assert(msg != NULL, __func__, __LINE__, __FILE__);
    bool ret = !is_computing();
    if (ret)
    {
        msg->type = MSG_SET_COMPUTE;
        msg->data.set_compute.c_re = comp.c_re;
        msg->data.set_compute.c_im = comp.c_im;
        msg->data.set_compute.d_re = comp.d_re;
        msg->data.set_compute.d_im = comp.d_im;
        msg->data.set_compute.n = comp.n;
        comp.done = false;
    }
    return ret;
}

bool compute(message *msg)
{
    my_assert(msg != NULL, __func__, __LINE__, __FILE__);
    if (!is_computing())
    {
        comp.cid = 0;
        comp.computing = true;
        comp.cur_x = comp.cur_y = 0;       //start compution of the whole image
        comp.chunk_re = comp.range_re_min; //upper-left corner
        comp.chunk_im = comp.range_im_max; //upper-left corner
        msg->type = MSG_COMPUTE;
    }
    else
    {
        comp.cid += 1;
        if (comp.cid < comp.nbr_chunks)
        {
            comp.cur_x += comp.chunk_n_re;
            comp.chunk_re += comp.chunk_n_re * comp.d_re;
            if (comp.cur_x >= comp.grid_w)
            {
                comp.cur_x = 0;
                comp.chunk_re = comp.range_re_min;
                comp.chunk_im += comp.chunk_n_im * comp.d_im;
                comp.cur_x = 0;
                comp.cur_y += comp.chunk_n_im;
            }
            msg->type = MSG_COMPUTE;
        }
    }
    if (comp.computing && msg->type == MSG_COMPUTE)
    {
        msg->data.compute.cid = comp.cid;
        msg->data.compute.re = comp.chunk_re;
        msg->data.compute.im = comp.chunk_im;
        msg->data.compute.n_re = comp.chunk_n_re;
        msg->data.compute.n_im = comp.chunk_n_im;
    }
    return is_computing();
}

void update_image(int w, int h, unsigned char *img)
{
    my_assert(img && comp.grid && w == comp.grid_w && h == comp.grid_h, __func__, __LINE__, __FILE__);
    for (int i = 0; i < w * h; i++)
    {
        const double t = 1. * comp.grid[i] / (comp.n + 1.0);
        *(img++) = 9 * (1 - t) * t * t * t * 255;               //R
        *(img++) = 15 * (1 - t) * (1 - t) * t * t * 255;        //G
        *(img++) = 8.5 * (1 - t) * (1 - t) * (1 - t) * t * 255; //B
    }
}

void update_data(const msg_compute_data *compute_data)
{
    my_assert(compute_data != NULL, __func__, __LINE__, __FILE__);
    if (compute_data->cid == comp.cid)
    {
        const int idx = comp.cur_x + compute_data->i_re + (comp.cur_y + compute_data->i_im) * comp.grid_w;
        if (idx >= 0 && idx < (comp.grid_w * comp.grid_h))
        {
            comp.grid[idx] = compute_data->iter;
        }
        if ((comp.cid + 1) >= comp.nbr_chunks && (compute_data->i_re + 1) == comp.chunk_n_re && (compute_data->i_im + 1) == comp.chunk_n_im)
        {
            comp.done = true;
            comp.computing = false;
        }
    }
    else
    {
        warn("Recieved chunk with unexpected chunk id (cid)");
    }
}

void clear_buffer(void)
{
    if (comp.grid)
    {
        for (int i = 0; i < comp.grid_w * comp.grid_h; i++)
        {
            comp.grid[i] = 0;
        }
    }
}

void reset_cid(void)
{
    comp.computing = false;
    comp.cid = 0;
}

void juli_comp()
{
    int iter = 0;
    double re_set = comp.range_re_min;
    double im_set = comp.range_im_max;
    for (int i = 0; i < comp.grid_h; i++)
    {
        re_set = comp.range_re_min;
        for (int r = 0; r < comp.grid_w; r++)
        {
            double re = re_set;
            double im = im_set;
            iter = 0;
            double z_abs = 0.0;
            while (z_abs < 2.0 && iter < comp.n)
            {
                //fprintf(stderr, "Compute data re: %f im: %f iter: %d x: %d y: %d \n",re, im, iter, r, i);
                double re_new = re * re - (im * im) + comp.c_re;
                im = 2 * re * im + comp.c_im;
                re = re_new;
                iter++;
                z_abs = sqrt((re * re) + (im * im));
            }
            //fprintf(stderr, "Compute data re: %f im: %f iter: %d x: %d y: %d \n",re, im, iter, r, i);
            comp.grid[(comp.grid_w) * i + r] = iter;
            re_set += comp.d_re;
        }
        im_set += comp.d_im;
    }
}

void animate()
{
    for (int an = 1; an < 100; an++)
    {
        double d = 0.5 - 0.01 * an;
        int iter = 0;
        double re_set = comp.range_re_min;
        double im_set = comp.range_im_max;
        for (int i = 0; i < comp.grid_h; i++)
        {
            re_set = comp.range_re_min;
            for (int r = 0; r < comp.grid_w; r++)
            {
                double re = re_set;
                double im = im_set;
                iter = 0;
                double z_abs = 0.0;
                while (z_abs < 2.0 && iter < comp.n)
                {
                    //fprintf(stderr, "Compute data re: %f im: %f iter: %d x: %d y: %d \n",re, im, iter, r, i);
                    double re_new = re * re - (im * im) + comp.c_re + d;
                    im = 2 * re * im + comp.c_im +d;
                    re = re_new;
                    iter++;
                    z_abs = sqrt((re * re) + (im * im));
                }
                //fprintf(stderr, "Compute data re: %f im: %f iter: %d x: %d y: %d \n",re, im, iter, r, i);
                comp.grid[(comp.grid_w) * i + r] = iter;
                re_set += comp.d_re;
            }
            im_set += comp.d_im;
        }
        gui_refresh();
    }
}
