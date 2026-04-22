package main

import (
    "fmt"
    "net/http"
    "time"
)

func fetchData(url string, ch chan<- string) {
    resp, err := http.Get(url)
    if err != nil {
        ch <- fmt.Sprintf("Error: %v", err)
        return
    }
    defer resp.Body.Close()
    ch <- fmt.Sprintf("Fetched %s (status: %d)", url, resp.StatusCode)
}

func task1() string {
    time.Sleep(100 * time.Millisecond)
    return "Task 1 done"
}

func task2() string {
    time.Sleep(100 * time.Millisecond)
    return "Task 2 done"
}

func main() {
    fmt.Println("=== Async Programming Demo ===")

    // Sequential async (slower)
    fmt.Println("Fetching sequentially...")
    resp, _ := http.Get("https://httpbin.org/get")
    fmt.Printf("First done! (status: %d)\n", resp.StatusCode)
    resp.Body.Close()

    // Parallel async (faster)
    fmt.Println("Fetching in parallel...")
    ch := make(chan string, 3)
    go fetchData("https://httpbin.org/get", ch)
    go fetchData("https://httpbin.org/get", ch)
    go fetchData("https://httpbin.org/get", ch)
    for i := 0; i < 3; i++ {
        fmt.Println(<-ch)
    }

    // Run functions in parallel
    fmt.Println("Running functions in parallel...")
    ch1 := make(chan string, 2)
    go func() { ch1 <- task1() }()
    go func() { ch1 <- task2() }()
    for i := 0; i < 2; i++ {
        fmt.Println(<-ch1)
    }
}