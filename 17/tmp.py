def trajectory_in_bucket(x0, y0, vx, vy, bounds):
    xpos = calc_x_pos(vx, x0)
    ypos = calc_y_pos(1, vy, y0)
    xb, yb = bounds
    idx = np.where(((ret[:, 0] >= xb[0]) & (ret[:, 0] <= xb[1])) & ((ret[:, 1] >= yb[0]) & (ret[:, 1] <= yb[1])))
    pass

