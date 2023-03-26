# Chapter 1. Basics

## 1.0 Methods

```
method Triple(x: int) returns (r: int) {
  var y := 2 * x;
  r := x + y;
}
```

#### Exercise 1.0

```
30
```

## 1.1 Assert Statements

```
method Triple(x: int) returns (r: int) {
  var y := 2 * x;
  r := x + y;
  assert r == 3 * x;
}
```

#### Exercise 1.1

## 1.2 Working with the Verifier

## 1.3 Controll Paths

```
method Triple(x: int) returns (r: int) {
  if x == 0 {
    r := 0;
  } else {
    var y := 2 * x;
    r := x + y;
  }
  assert r == 3 * x;
}
```

```
method Triple(x: int) returns (r: int) {
  if {
    case x < 18 =>
      var a, b := 2 * x, 4 * x;
      r := (a + b) / 2;
    case 0 <= x =>
      var y := 2 * x;
      r := x + y;
  }
  assert r == 3 * x;
}
```

## 1.4 Method Contracts

```
method Triple(x: int) returns (r: int) {
  var y := 2 * x;
  r := x + y;
  assert r == 3 * x;
}

method Caller() {
  var t := Triple(18);
  assert t < 100; // -> Error!
}
```

verifier は `Triple` の中身は見ないし、実行して検証もしない。

```
method Triple(x: int) returns (r: int)
  ensures r == 3 * x
{
  var y := 2 * x;
  r := x + y;
  assert r == 3 * x;
}

method Caller() {
  var t := Triple(18);
  assert t < 100; // -> OK
}
```

#### Exercise 1.4
```
method Triple(x: int) returns (r: int)
  requires x % 2 == 0 // この行が無いとensuresがエラー
  ensures r == 3 * x
{
  var y := x / 2;
  r := 6 * y;
}
```

#### Exercise 1.5

```
requires x == 0 || x == 18
```

#### Exercise 1.6

```
method Min(x: int, y: int) returns (m: int)
  ensures m <= x && m <= y
{
  if x <= y {
    m := x - 1;
  } else {
    m := y - 1;
  }
}
```

### Exercise 1.7

```
method MaxSum(x: int, y: int) returns (s: int, m: int)
  ensures x <= m && y <= m
  ensures m == x || m == y
  ensures s == x + y
{
  if x <= y {
    m := y;
  } else {
    m := x;
  }
  s := x + y;
}
```

### Exercise 1.8

```
method MaxSum(x: int, y: int) returns (s: int, m: int)
  ensures x <= m && y <= m
  ensures m == x || m == y
  ensures s == x + y
{
  if x <= y {
    m := y;
  } else {
    m := x;
  }
  s := x + y;
}

method ReconstructFromMaxSum(s: int, m: int) returns (x: int,y: int)
  requires s <= 2 * m
  ensures s == x + y
  ensures (m == x || m == y) && x <= m && y <= m
{
  x := m;
  y := s - m;
}

method TestMaxSum(x: int, y: int) {
  var s, m := MaxSum(x, y);
  var xx, yy := ReconstructFromMaxSum(s, m);
  assert (x == xx && y == yy) || (x == yy && y == xx);
}
```

## 1.5 Function

```
function Average(a: int, b: int): int {
  (a + b) / 2
}
```

function は事前条件や事後条件を書くのに便利。

```
method Triple'(x: int) returns (r: int)
  ensures Average(r, 3 * x) == 3 * x
{
  r := 3 * x;
}
```

#### Exercise 1.9

```
method Triple'(x: int) returns (r: int)
  ensures Average(r, 3 * x) == 3 * x
{
  r := 3 * x + 1;
}
```

戻り値型が `bool` の function を predicate という。
```
predicate IsEven(x: int) {
  x % 2 == 0
}
```

## 1.6 Compiled versus Ghost

事前条件や事後条件、assertion は ghost であり、実行時には消去される。

#### Exercise 1.10

```
method Triple(x: int) returns (r: int)
  ensures r == 3 * x
{
  var y := x * 2;
  r := x + y;
  ghost var a, b := DoubleQuadruple(x);
  assert a <= r <= b || b <= r <= a;
}

ghost method DoubleQuadruple(x: int) returns (a: int, b: int)
  ensures a == 2 * x && b == 4 * x
{
  a := 2 * x;
  b := 4 * x;
}
```

## 1.7 Summary

#### Exercise 1.11

method は ensures に書かれたことしか証明に使えない。
function は式として展開される？

```
function F(): int {
  29
}

method M() returns (r: int)
  ensures r == 29
{
  r := 29;
}

method Caller2()
{
  var a := F();
  var b := M();
  assert a == 29;
  assert b == 29;
}
```

Dafny の int には最大値最小値は無い。無限長の整数。

