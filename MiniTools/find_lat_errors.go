//처리 속도 이슈를 해결하기 위해 Golang으로 구현

package main

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "os"
    "path/filepath"
)

func main() {
    // 1. 폴더 내에 존재하는 json 파일을 모두 불러와 리스트를 생성
    files, err := filepath.Glob("*.json")
    if err != nil {
        panic(err)
    }

    // 2. 생성된 리스트의 json을 순차적으로 불러와서 "latitude" 속성이 100보다 큰 경우를 선별
    for _, file := range files {
        f, err := os.Open(file)
        if err != nil {
            fmt.Printf("Failed to open file %s: %v\n", file, err)
            continue
        }
        defer f.Close()

        var data map[string]interface{}
        decoder := json.NewDecoder(f)
        err = decoder.Decode(&data)
        if err != nil {
            fmt.Printf("Failed to decode file %s: %v\n", file, err)
            continue
        }

        if latitude, ok := data["latitude"].(float64); ok {
            if latitude > 100 {
                // 3. 100보다 큰 경우 파일명을 "error_latitude.json"에 순차적으로 저장
                errFile, err := os.OpenFile("error_latitude.json", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
                if err != nil {
                    fmt.Printf("Failed to open file error_latitude.json: %v\n", err)
                    continue
                }
                defer errFile.Close()

                errFile.WriteString(file + "\n")
            }
        }
    }
}
