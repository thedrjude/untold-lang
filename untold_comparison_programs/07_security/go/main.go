package main

import (
    "crypto/hmac"
    "crypto/rand"
    "crypto/sha256"
    "crypto/sha512"
    "encoding/base64"
    "encoding/hex"
    "fmt"
)

func main() {
    password := "MySecurePassword123"

    // SHA256 hashing
    h := sha256.Sum256([]byte(password))
    fmt.Printf("SHA256: %s\n", hex.EncodeToString(h[:]))

    // SHA512 hashing
    h512 := sha512.Sum512([]byte(password))
    fmt.Printf("SHA512: %s\n", hex.EncodeToString(h512[:]))

    // HMAC
    m := hmac.New(sha256.New, []byte("secret_key"))
    m.Write([]byte(password))
    fmt.Printf("HMAC-SHA256: %s\n", hex.EncodeToString(m.Sum(nil)))

    // Base64 encoding
    encoded := base64.StdEncoding.EncodeToString([]byte(password))
    fmt.Printf("Base64: %s\n", encoded)

    // Constant-time comparison
    stored := sha256.Sum256([]byte("password"))
    current := sha256.Sum256([]byte(password))
    if hmac.Equal(stored[:], current[:]) {
        fmt.Println("Secure match!")
    }

    // Verify hash
    computed := sha256.Sum256([]byte(password))
    if hmac.Equal(computed[:], computed[:]) {
        fmt.Println("Hash verified!")
    }

    // Random token generation
    token := make([]byte, 32)
    rand.Read(token)
    fmt.Printf("Random token: %s\n", hex.EncodeToString(token))
}