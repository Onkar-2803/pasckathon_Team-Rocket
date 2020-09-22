def green_time(density_final):

    final_density = density_final
    if(final_density<=0.3):
        sginal_green_time=20
    elif(final_density<=0.6 & final_density>0.3):
        signal_green_time= 40
    else:
        signal_green_time = 60

    return signal_green_time
