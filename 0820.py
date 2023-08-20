# 将双色球的中奖号码转换为整数，更方便进行预测
def binary_to_decimal(positions):

    binary_list_red = ['0'] * 33
    binary_list_blue = ['0'] * 16
    for pos_red in positions[0:-1]:
        binary_list_red[pos_red - 1] = '1'
    binary_list_blue[positions[-1] - 1] = '1'
    binary_list = binary_list_red + binary_list_blue
    print('in------',binary_list)
    decimal_num = 0
    for i, bit in enumerate(binary_list, start=1):
        if bit == '1':
            decimal_num += 2 ** (len(binary_list) - i)
    return decimal_num

def decimal_to_binary(decimal_num):
    binary_num = bin(decimal_num)[2:]  # 将十进制数转换为二进制字符串，去掉前缀'0b'
    binary_list = list(binary_num.zfill(49))  # 将二进制字符串填充到长度为49
    # binary_length=33
    # binary_list = list(format(decimal_num, f'0{binary_length}b'))

    positions = [i+1 for i, bit in enumerate(binary_list) if bit == '1']  # 找出值为1的位的位置
    positions_inverse=positions[0:-1] + [positions[-1] - 33]
    return positions_inverse





positions = [11,17,21,23,3,4,16]
result = binary_to_decimal(positions)
print(result)



decimal_num = result  # 一个示例的十进制数
positions_inverse = decimal_to_binary(decimal_num)

print('-----out',positions_inverse)







# binary_list = ['0'] * 33
# positions = [1,2,3,4,30,31,32,33]
# for pos in positions:
#     binary_list[pos - 1] = '1'
# print(binary_list)
# result = binary_to_decimal(binary_list)
# print(result)
#
#
# decimal_num = result  # 一个示例的十进制数
# result1 = decimal_to_binary(decimal_num)
# print(result1)
