#!/bin/zsh

HOST="Mac:4200"
COOKIE_FILE="cookies.txt"

echo "===== Test 1: Login with correct credentials ====="
curl -s -c $COOKIE_FILE -d "username=bezos&password=amazon" http://$HOST | grep -q "Welcome!" && echo "PASS" || echo "FAIL"

echo "\n===== Test 2: Login with incorrect password ====="
curl -s -d "username=bezos&password=wrongpass" http://$HOST | grep -q "Bad user/pass!" && echo "PASS" || echo "FAIL"

echo "\n===== Test 3: Missing password ====="
curl -s -d "username=bezos" http://$HOST | grep -q "Bad user/pass!" && echo "PASS" || echo "FAIL"

echo "\n===== Test 4: Access with valid cookie ====="
curl -s -b $COOKIE_FILE http://$HOST | grep -q "Welcome!" && echo "PASS" || echo "FAIL"

echo "\n===== Test 5: Access with invalid cookie ====="
curl -s -H "Cookie: token=invalidtoken" http://$HOST | grep -Eq "Bad user/pass|Please login" && echo "PASS" || echo "FAIL"

echo "\n===== Test 6: Logout with valid cookie ====="
curl -s -b $COOKIE_FILE -d "action=logout" http://$HOST | grep -q "Logged out successfully" && echo "PASS" || echo "FAIL"

echo "\n===== Test 7: GET without cookie ====="
curl -s http://$HOST | grep -q "Please login" && echo "PASS" || echo "FAIL"
