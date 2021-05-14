nums = list(map(int, input().split()))
count = 0
length = 0
l = 0
c = 0
k = 0
for i in range(len(nums)-1):

    if nums[i] % 2 == 0:
        if k == 0:
            l = 1
            c += nums[i]
            k = 1
        if nums[i+1] % 2 == 0 and nums[i] < nums[i+1]:
            c += nums[i+1]
            l += 1

        if l > length:
            length = l
            count = c
        elif l == length and c > count:
            count = c

        if nums[i+1] % 2 != 0 or nums[i] >= nums[i+1]:
            c = 0
            l = 0
            k = 0

print(length)
print(count)

