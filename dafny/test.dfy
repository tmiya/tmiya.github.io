method Abs(x: int) returns (y: int)
  // Add a precondition here.
  ensures 0 <= y
  ensures 0 <= x ==> y == x
  ensures x < 0 ==> y == -x
{
  if x < 0 {
    y := -x;
  } else {
    y := x;
  }
}

method Max(a: int, b: int) returns (c: int)
  ensures a == c || b == c
  ensures a <= c && b <= c
{
  if a < b {
    return b;
  } else {
    return a;
  }
}

method Testing()
{
  var v := Max(2,3);
  assert 0 <= v;
}

method m(n: nat)
{
  var i: int := 0;
  while i < n
    invariant 0 <= i <= n
  {
    i := i + 1;
  }
  assert i == n;
}

function fib(n: nat): nat
{
  if n == 0 then 0
  else if n == 1 then 1
  else fib(n - 1) + fib(n - 2)
}
method ComputeFib(n: nat) returns (b: nat)
  ensures b == fib(n)
{
  if n == 0 { return 0; }
  var i := 1;
  var a := 0;
  b := 1;
  while i < n
    invariant 0 < i <= n
    invariant a == fib(i - 1)
    invariant b == fib(i)
  {
    a, b := b, a + b;
    i := i + 1;
  }
}

method m2()
{
  var i, n := 0, 20;
  while i != n
    invariant 0 <= i <= 20
    decreases n - i
  {
    i := i + 1;
  }
}

method Find(a: array<int>, key: int) returns (index: int)
  ensures 0 <= index ==> index < a.Length && a[index] == key
  ensures index < 0 ==> forall k :: 0 <= k < a.Length ==> a[k] != key
{
  index := 0;
  while index < a.Length
    invariant 0 <= index <= a.Length
    invariant forall k :: 0 <= k < index ==> a[k] != key
  {
    if a[index] == key { return; }
    index := index + 1;
  }
  index := -1;
}

method FindMax(a: array<int>) returns (i: int)
  requires 0 < a.Length
  ensures 0 <= i < a.Length
  ensures forall k :: 0 <= k < a.Length ==> a[k] <= a[i]
{
  i := 0;
  var k := 0;
  while k < a.Length
    invariant 0 <= i < a.Length
    invariant 0 <= k <= a.Length
    invariant forall j :: 0 <= j < k ==> a[j] <= a[i]
  {
    if a[k] > a[i] { i := k; }
    k := k + 1;
  }
}

predicate sorted(a: array<int>)
  reads a
{
  if a.Length == 0 then false
  else (
       forall j, k :: 0 <= j < k < a.Length ==> a[j] <= a[k]
                      )
}

method Index(n: int) returns (i: int)
  requires 1 <= n
  ensures 0 <= i < n
{
  i := n / 2;
}

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

function Average(a: int, b: int): int {
  (a + b) / 2
}

method Triple'(x: int) returns (r: int)
  ensures Average(r, 3 * x) == 3 * x
{
  r := 3 * x + 1;
}

predicate IsEven(x: int) {
  x % 2 == 0
}

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

function F(): int {
  29
}

method M2() returns (r: int)
  ensures r == 29
{
  r := 29;
}

method Caller2()
{
  var a := F();
  var b := M2();
  assert a == 29;
  assert b == 29;
}