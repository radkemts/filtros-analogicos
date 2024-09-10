if __name__ == "__main__":
    import butterworth

    a_pass = -1
    a_stop = -30
    w_pass = 1
    w_stop = 2

    result = butterworth.normalized_low_pass(a_pass, a_stop, w_pass, w_stop)
    for key, value in result.items():
        print(f"{key}: {value}")