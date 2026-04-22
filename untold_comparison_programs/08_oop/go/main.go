package main

import "fmt"

type Person struct {
    Name string
    Age  int
}

func (p *Person) greet() {
    fmt.Printf("Hi, I am %s and I'm %d years old!\n", p.Name, p.Age)
}

type Developer struct {
    Person
    Language string
}

func (d *Developer) introduce() {
    fmt.Printf("I code in %s\n", d.Language)
}

func main() {
    // Create person object
    p := Person{Name: "Untold", Age: 2}
    p.greet()

    // Modify properties
    p.Age = 3
    fmt.Printf("Updated age: %d\n", p.Age)

    // Use inherited behavior
    dev := Developer{
        Person:   Person{Name: "Dev", Age: 25},
        Language: "Go",
    }
    dev.greet()
    dev.introduce()
}