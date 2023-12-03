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