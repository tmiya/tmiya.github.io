# One D&D Character Builder

## Design policy

* Race, Clazz は 抽象クラスとして扱い、Elf とか Bard のように具象クラスを持つ
* Model クラスに対して View クラスを定義する。コレクションクラスも持つ。
   * Char -> CharView 
   * Race -> RaceView, Races
   * Clazz -> ClassView, Classes
   * Elf -> ElfView
   * Bard -> BardView
   * Levels -> LevelsView
* 自分の View クラスで閉じない範囲のイベントは、
   * Char に update する
   * Char の内容に整合するように CharView で表示を update する
      * CharView.update は 各page.update を呼び出す

```mermaid
sequenceDiagram
	loop True
		main_loop ->>+ window: read()
		window ->>- main_loop: event, values
		main_loop ->>+ root_view: handler(w,e,v)
		root_view ->>+ root: handler(e,v)
		root ->>+ child: handler(e,v)
		child ->>- root: 
		root ->>- root_view: 
		root_view ->>+ root_view: update(w)
		root_view ->>+ child_view: update(w)
		child_view ->>- root_view: 
		root_view ->>- main_loop: 
		main_loop ->>+ root: update(window)
		root ->>+ child: update(window)
		child ->>- root: 
		root ->>+ root_view: update(window)
		root_view ->>- root: 
		root ->>- main_loop: 
	end
```

    
    ```mermaid
sequenceDiagram
    participant cook as コック
    participant kitchenware1 as フライパン

    cook ->>+ kitchenware1: ハンバーグを焼く
    Note over kitchenware1: 8分ほど待つ
    kitchenware1 -->>- cook: 焼き上がり
    Note right of kitchenware1: 竹串を刺して透明な汁が出たら完成
```