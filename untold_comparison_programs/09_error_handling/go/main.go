package main

import (
    "fmt"
    "os"
    "io/ioutil"
)

func main() {
    fmt.Println("=== Error Handling Demo ===")

    // Success case
    try := func() {
        err := ioutil.WriteFile("test.txt", []byte("Hello"), 0644)
        if err != nil {
            fmt.Println("Error:", err)
            return
        }
        content, err := ioutil.ReadFile("test.txt")
        if err != nil {
            fmt.Println("Error:", err)
            return
        }
        fmt.Printf("Success: %s\n", content)
    }
    try()

    defer func() {
        fmt.Println("Cleanup: deleting file")
        os.Remove("test.txt")
    }()

    // Error case
    defer func() {
        fmt.Println("Done with error demo")
    }()

    _, err := ioutil.ReadFile("nonexistent.txt")
    if err != nil {
        fmt.Printf("Caught error: %v\n", err)
    }
}