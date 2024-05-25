lb_5 = 3
include = True
num_cols = lb_5

if include:
    num_cols += 1

arr_5 = np.array([np.nan, np.nan, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0])

arr_5_size = arr_5.size

a_arr_5 = np.where(np.isnan(arr_5))[0].size

p_arr_5 = np.full((arr_5_size, num_cols), np.nan)
g_arr_5 = arr_5[lb_5:].size

s_pa = lb_5 + a_arr_5

for col in range(num_cols):
    p_arr_5[s_pa:, col] = arr_5[col + a_arr_5 : g_arr_5 + col]

p_arr_5