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
