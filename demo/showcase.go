// Package main is a tiny worker pool, used to show off Go colors.
package main

import (
	"fmt"
	"sync"
	"time"
)

type Job struct {
	ID    int
	Delay time.Duration
}

type Runner interface {
	Run(job Job) (string, error)
}

const workers = 3

func worker(id int, jobs <-chan Job, out chan<- string, wg *sync.WaitGroup) {
	defer wg.Done()
	for j := range jobs {
		time.Sleep(j.Delay)
		out <- fmt.Sprintf("worker %d finished job %d", id, j.ID)
	}
}

func main() {
	jobs := make(chan Job, 5)
	out := make(chan string, 5)
	var wg sync.WaitGroup

	for i := 1; i <= workers; i++ {
		wg.Add(1)
		go worker(i, jobs, out, &wg)
	}
	for n := 0; n < 5; n++ {
		jobs <- Job{ID: n, Delay: 10 * time.Millisecond}
	}
	close(jobs)
	wg.Wait()
	close(out)
	for line := range out {
		fmt.Println(line)
	}
}
