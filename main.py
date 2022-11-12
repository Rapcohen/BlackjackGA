import time

from ga import algo

if __name__ == "__main__":
    start_time = time.time()
    algo.evolve()
    print("--- execution time: %.2f seconds ---" % (time.time() - start_time))
