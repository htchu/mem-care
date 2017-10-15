package main

import (
	"fmt"
	"time"
	"strings"
	"gopkg.in/zabawaba99/firego.v1"
	"log"
	"unicode"
	"strconv"
)

func main(){
	loc, _ := time.LoadLocation("Asia/Taipei")
	layoutStr := "1月 2, 2006 15:04:05" //2016-1-2 15:04:05是golang出生時間
	/*testStr := "\"8月 31, 2017 16:50:38\""
	
	timeStr, _ := strconv.Unquote(testStr)
	t, _  := time.ParseInLocation(layoutStr, timeStr, loc )
	fmt.Println(t)*/
	//names := [...]string{"秀子", "許秀琴", "秀琴", "蕭妍", "刑簫研", "刑蕭研", "賴黃省", "王省", "黃省", "玉爵中度", "玉爵", "張圓", "張員"}
	/*
	validSet := make(map[string]bool)
	for _, name := range names {
        validSet[name] = true
	}*/
		
	alias := make(map[string]string)
	alias["秀子"] = "秀子"
	alias["許秀琴"] = "秀子"
	alias["秀琴"] = "秀子"
	alias["蕭妍"] = "蕭妍"
	alias["刑簫研"] = "蕭妍"
	alias["刑蕭研"] = "蕭妍"
	alias["賴黃省"] = "黃省"
	alias["王省"] = "黃省"
	alias["黃省"] = "黃省"
	alias["玉爵中度"] = "玉爵"
	alias["玉爵"] = "玉爵"
	alias["張圓"] = "張員"
	alias["張員"] = "張員"
	//m["test"] = t
	testTime := make(map[string]time.Time)


	fs := func(c rune) bool {
		return !unicode.IsLetter(c) && !unicode.IsNumber(c)
	}
	f := firego.New("https://xfire1-37855.firebaseio.com", nil)
	var tests = f.Child("tests")
	var mymap map[string]interface{}
	//var mymap map[string]string
	if err := tests.Value(&mymap); err != nil {
		log.Fatal(err)
	}
	
	for k, v := range mymap {	
		/*a :=make([]byte, 4, 4)
		copy(a[:], k)
		/*fmt.Println("k:", []byte(k), "a:", a)
		fmt.Printf("%d=", len(k))
		for i:=0; i< len(k); i++{
			fmt.Printf("%d ", k[i])
		}*/
		//username := string(a[:]) 

		if _, ok := alias[k]; !ok {
			continue
		} 
		
			
		switch vv := v.(type) {
		case string:
			fmt.Println(k, "is string", vv)
		case int:
			fmt.Println(k, "is int", vv)
		case float64:
			fmt.Println(k,"is float64",vv)
		case []interface{}:
			//fmt.Println(k, "is an array:")
			for i, u := range vv {
				switch uu := u.(type) {
				case string:
					fmt.Println(k, ";", i, ";", uu)
					timeStr, _ := strconv.Unquote(uu)
					timeStr = strings.Trim(timeStr, " 下午")
					timeStr = strings.Trim(timeStr, " 上午")
					t, _  := time.ParseInLocation(layoutStr, timeStr, loc )
					testno := k+"-"+strconv.Itoa(i);//serial
                    testTime[testno] = t
				case int:
					fmt.Println(i, "is int",uu)
				case float64:
					fmt.Println(i,"is float64",uu)
				case []interface{}:
					fmt.Println(i, "is an array:")
					for j, w := range uu {
						switch ww := w.(type) {
						case string:
							fmt.Println(j, "is string", ww)
						case int:
							fmt.Println(j, "is int",ww)
						case float64:
							fmt.Println(j,"is float64",ww)
						case []interface{}:						
							fmt.Println(j, "{}", ww)
						}
					}
				}
			}
		default:
			fmt.Println(k, "is of a type I don't know how to handle")
		}
		
	}
	fmt.Println(testTime)

	var games = f.Child("games")
	//var mymap map[string]string
	if err := games.Value(&mymap); err != nil {
		log.Fatal(err)
	}
	for k, v := range mymap {
		serial := strings.TrimSpace(k)
		tt, ok := testTime[serial]
		if !ok {
			continue
		} 
		switch vv := v.(type) {
		case string:
			fmt.Println(k, "is string", vv)
		case int:
			fmt.Println(k, "is int", vv)
		case float64:
			fmt.Println(k,"is float64",vv)
		case []interface{}:
			//fmt.Println(k, "is an array:")
			var temp [100]string
			var start int64 = 0
			var end int64 = 0
			var count int = 0
			for i, u := range vv {
				switch uu := u.(type) {
				case string:
					fmt.Println(serial, ";", i, ";", uu)
					ss :=strings.FieldsFunc(uu, fs)
					num, err := strconv.ParseInt(ss[6], 10, 64)
					if err != nil {
						panic(err)
					}
					if (count ==0){
						start = num
					}
					end = num
					temp[count] = uu
					count++
				case int:
					fmt.Println(i, "is int",uu)
				case float64:
					fmt.Println(i,"is float64",uu)
				case []interface{}:
					fmt.Println(i, "is an array:")
					for j, w := range uu {
						switch ww := w.(type) {
						case string:
							fmt.Println(j, "is string", ww)
						case int:
							fmt.Println(j, "is int",ww)
						case float64:
							fmt.Println(j,"is float64",ww)
						case []interface{}:						
							fmt.Println(j, "{}", ww)
						}
					}
				}
			}
			period := end - start;
			if (count > 1 && period >1000){
				fmt.Println(tt, "Worked tries=",count," period=", period/1000, "secconds" )	
			}else{
				fmt.Println("Not    tries=",count," period=", period/1000, "secconds" )
			}

		default:
			fmt.Println(k, "is of a type I don't know how to handle")
		}
	}
 }