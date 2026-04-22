package main

import (
    "fmt"
    "io/ioutil"
    "net/http"
    "strings"
)

func main() {
    // GET request
    fmt.Println("Fetching data...")
    resp, err := http.Get("https://api.github.com")
    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    defer resp.Body.Close()
    body, _ := ioutil.ReadAll(resp.Body)
    fmt.Printf("Status: %d\n", resp.StatusCode)
    fmt.Printf("Body length: %d\n", len(body))

    // POST request
    jsonStr := strings.NewReader(`{"key":"value"}`)
    resp2, err := http.Post("https://httpbin.org/post", "application/json", jsonStr)
    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    defer resp2.Body.Close()
    fmt.Printf("POST Status: %d\n", resp2.StatusCode)
}