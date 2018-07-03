import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing as mp
import logging
import queue

logger = mp.log_to_stderr(logging.INFO)

# Only does something to in_image, doesn't access anything else
def do_work(in_image):
    logger.info('Processing in_image')
    for x in range(100000):
        out_image = in_image[::-1, ::-1]
    out_queue.put(out_image)

# Update the output image and display if needed
out_all = np.zeros((256, 256))


def pool_initializer(out_queue_):
    # Setup out_queue as a global variable *in the worker subprocesses*
    global out_queue
    out_queue = out_queue_


def animate():
    global out_all
    try:
        out_image = out_queue.get_nowait()
    except queue.Empty:
        pass
    else:
        logger.info("Updating")
        out_all += out_image
        im.set_data(out_all)
        fig.canvas.draw()  # redraw the canvas
    win.after(100, animate)

if __name__ == '__main__':
    out_queue = mp.Queue()
    logger.info("Starting pool")
    pool = mp.Pool(initializer=pool_initializer, initargs=(out_queue, ))
    work = [np.random.random((256, 256)) for f in range(20)]
    for o in work:
        pool.apply_async(do_work, [o])
    pool.close()

    fig, ax = plt.subplots()
    win = fig.canvas.manager.window
    # Output image
    im = plt.imshow(out_all, vmin=0, vmax=1)

    # Register a function to be run once
    win.after(100, animate)
    plt.show()
    logger.info("Done")