from math import sqrt
# All decimal 3 places

# Function to compute mean
def mean(first_list):
    sum3 = 0
    for i in first_list:
        if isinstance(i,(int,float)):
            sum3 = sum3 + i
        else:
            return 0

    mean_value = sum3/len(first_list)
    return mean_value


# Function to compute median. You cant use Python functions
def median(first_list):
    for i in first_list:
        if isinstance(i,(int,float)):
            pass
        else:
            return 0
    temp = 0
    for i in range (len(first_list)):
        for j in range(i + 1, len(first_list)):
            if(first_list[i] > first_list[j]):
                temp = first_list[i]
                first_list[i] = first_list[j]
                first_list[j] = temp

    k = len(first_list)
    if k%2 == 0:
        median_value = (first_list[k//2]+first_list[(k//2)-1])/2
    else:
        median_value = first_list[(k//2)]

    return median_value


# Function to compute Standard deviation. You cant use Python functions
def standard_deviation(first_list):
    for i in first_list:
        if isinstance(i,(int,float)):
            pass
        else:
            return 0
    V_list = list()
    V_mean = mean(first_list)
    for i in range(len(first_list)):
        V_list.append((first_list[i]-V_mean)**2)
    V_sum = summation(V_list)
    variance_value = 0
    variance_value = V_sum/len(first_list)
    standard_deviation_value = sqrt(variance_value)
    return standard_deviation_value


# Function to compute variance. You cant use Python functions
def variance(first_list):
    for i in first_list:
        if isinstance(i,(int,float)):
            pass
        else:
            return 0
    V_list = list()
    V_mean = mean(first_list)
    for i in range(len(first_list)):
        V_list.append((first_list[i]-V_mean)**2)
    V_sum = summation(V_list)
    variance_value = 0
    variance_value = V_sum/len(first_list)
    return variance_value


# Function to compute RMSE. You cant use Python functions
def rmse(first_list, second_list):
    sum2 = 0
    if len(first_list) == len(second_list):
        for i in range(len(first_list)):
            if isinstance(first_list[i],(int,float)) and isinstance(second_list[i],(int,float)):
                sum2 = sum2 + ((first_list[i]-second_list[i])**2)
            else:
                return 0
    else:
        return 0
    mse_value = 0
    mse_value = sum2/len(first_list)
    rmse_value = sqrt(mse_value)
    return rmse_value


# Function to compute mse. You cant use Python functions
def mse(first_list, second_list):
    sum1 = 0
    if len(first_list) == len(second_list):
        for i in range(len(first_list)):
            if isinstance(first_list[i],(int,float)) and isinstance(second_list[i],(int,float)):
                sum1 = sum1 + ((first_list[i]-second_list[i])**2)
            else:
                return 0
    else:
        return 0
    mse_value = 0
    mse_value = sum1/len(first_list)
    return mse_value


# Function to compute mae. You cant use Python functions
def mae(first_list, second_list):
    mae_list = list()
    if len(first_list) == len(second_list):
        for i in range(len(first_list)):
            if isinstance(first_list[i],(int,float)) and isinstance(second_list[i],(int,float)):
                mae_list.append(abs(first_list[i]-second_list[i]))
            else:
                return 0
    else:
        return 0
    mae_value = 0
    mae_value = summation(mae_list)/len(first_list)
    return mae_value


# Function to compute NSE. You cant use Python functions
def nse(first_list, second_list):
    mae_list = list()
    V_list = list()
    mean_value = mean(first_list)
    if len(first_list) == len(second_list):
        for i in range(len(first_list)):
            if isinstance(first_list[i],(int,float)) and isinstance(second_list[i],(int,float)):
                mae_list.append((first_list[i]-second_list[i]) ** 2)
                V_list.append((first_list[i]-mean_value)**2)
            else:
                return 0
    else:
        return 0
    mae_sum = summation(mae_list)
    V_sum = summation(V_list)
    nse_value = 0
    nse_value = (1-(mae_sum/V_sum))
    return nse_value


# Function to compute Pearson correlation coefficient. You cant use Python functions
def pcc(first_list, second_list):
    a_mean = mean(first_list)
    b_mean = mean(second_list)
    num = list()
    A_list = list()
    B_list = list()
    if len(first_list) == len(second_list):
        for i in range(len(first_list)):
            if isinstance(first_list[i],(int,float)) and isinstance(second_list[i],(int,float)):
                num.append((first_list[i]-a_mean)*(second_list[i]-b_mean))
                A_list.append((first_list[i]-a_mean)**2)
                B_list.append((second_list[i]-b_mean)**2)
            else:
                return 0

    else:
        return 0
    num_sum = summation(num)
    A_sum = summation(A_list)
    B_sum = summation(B_list)
    pcv = 0
    if A_sum==0 or B_sum==0:
        return 0
    else:
        pcv = num_sum/(sqrt(A_sum)*sqrt(B_sum))
    return pcv


# Function to compute Skewness. You cant use Python functions
def skewness(first_list):
    for i in first_list:
        if isinstance(i,(int,float)):
            pass
        else:
            return 0
    a_mean = mean(first_list)
    A_list = list()
    std_val = standard_deviation(first_list)
    for i in range(len(first_list)):
        if std_val !=0:
            A_list.append(((first_list[i]-a_mean)/std_val)**3)
        else:
            return 0
    A_sum = summation(A_list)
    skewness_val = 0
    skewness_val = A_sum/len(first_list)
    return skewness_val

def sorting(first_list):
    s_list = first_list[:]
    for i in range(len(s_list)):
        for j in range(len(s_list)-i-1):
            if s_list[j] > s_list[j+1]:
                s_list[j],s_list[j+1] = s_list[j+1],s_list[j]
    return s_list


# Function to compute Kurtosis. You cant use Python functions
def kurtosis(first_list):
    for i in first_list:
        if isinstance(i,(int,float)):
            pass
        else:
            return 0
    a_mean = mean(first_list)
    AA_list = list()
    std_val = standard_deviation(first_list)
    for i in range(len(first_list)):
        if std_val !=0:
            AA_list.append(((first_list[i]-a_mean)/std_val)**4)
        else:
            return 0
    AA_sum = summation(AA_list)
    kurtosis_value = 0
    kurtosis_value = AA_sum/len(first_list)
    return kurtosis_value


# Function to compute sum. You cant use Python functions
def summation(first_list):
    summation_value = 0
    for i in first_list:
        if isinstance(i,(int,float)):
            summation_value = summation_value + i
        else:
            return 0
    return summation_value
