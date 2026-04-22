package main

import (
    "fmt"
    "os"
    "io/ioutil"
)

func main() {
    err := ioutil.WriteFile("data.txt", []byte("Hello from Go!"), 0644)
    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    fmt.Println("File written!")

    content, err := ioutil.ReadFile("data.txt")
    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    fmt.Printf("Content: %s\n", content)

    _, err = os.Stat("data.txt")
    if err == nil {
        fmt.Println("data.txt exists!")
    }

    err = os.Remove("data.txt")
    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    fmt.Println("File deleted!")
}