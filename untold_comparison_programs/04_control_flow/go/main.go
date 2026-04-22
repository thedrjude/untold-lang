package main

import "fmt"

func main() {
    score := 85

    // If-else
    if score >= 90 {
        fmt.Println("Grade: A")
    } else if score >= 80 {
        fmt.Println("Grade: B")
    } else if score >= 70 {
        fmt.Println("Grade: C")
    } else {
        fmt.Println("Grade: F")
    }

    // For loop
    fmt.Println("Counting:")
    for i := 0; i < 5; i++ {
        fmt.Println(i)
    }

    // While-like loop
    counter := 0
    for counter < 3 {
        fmt.Printf("While: %d\n", counter)
        counter++
    }
}