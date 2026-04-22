package main

import "fmt"

func main() {
    name := "Untold"
    fmt.Printf("Name: %s\n", name)

    version := 2.1
    fmt.Printf("Version: %v\n", version)

    isAwesome := true
    if isAwesome {
        fmt.Println("Untold is awesome!")
    }

    const PI = 3.14159
    fmt.Printf("PI: %v\n", PI)

    numbers := []int{1, 2, 3, 4, 5}
    fmt.Printf("Numbers: %v\n", numbers)
    fmt.Printf("Count: %d\n", len(numbers))

    data := map[string]string{"name": "Untold", "version": "2.1"}
    fmt.Printf("Data: %v\n", data)
    fmt.Printf("Get name: %s\n", data["name"])
}