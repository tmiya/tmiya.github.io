# OCaml Programming: Correct + Efficient + Beautiful

このページは [OCaml Programming: Correct + Efficient + Beautiful](https://cs3110.github.io/textbook/ocaml_programming.pdf) の勉強メモのページです。


## Install OPAM

OCaml 4.14.0 が選択肢に出ないので 4.12.0 でとりあえず妥協。

```
$ brew install opam
$ opam init --bare -a -y
$ opam switch list-available
$ opam switch create . ocaml-base-compiler.4.12.0
$ eval $(opam env)
$ ocaml --version
The OCaml toplevel, version 4.12.0
$ which ocaml  
~/tmiya.github.io/OCaml/cs3110/_opam/bin/ocaml
$ opam install -y utop odoc ounit2 qcheck bisect_ppx menhir
```

http://erratique.ch/ の証明書エラーで install が失敗する。

```
http://erratique.ch/software/react/releases/react-1.2.1.tbz\" exited with code 5 \"ERROR: cannot verify erratique.ch's certificate, issued by 'CN=R3,O=Let\\'s Encrypt,C=US':\")")
```
