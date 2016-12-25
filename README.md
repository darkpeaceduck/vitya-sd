### Требования : 
  
  - python 3.5 lib
  
 ### Запуск : 
  - add src folder to PYTHONPATH, 
  - run shell as python3.5 src/game/main.py [Level]

  например python3.5 game/main.py field

  
 ### Архитектура
 
 #### Описание
 
  - actions.py - описывает действия объектов на мир
  - action_makers.py - описывает стратегии поведения объктов (стратегия + composite)
  - characters.py - описывает характеристики и строение II и игрока (builder + сингтон + factory method)
  - field.py - описывает игровое поле
  - gfx.py - описывает графику + io
  - items.py - описывает предметы, которые можно подбирать
  - logic.py - описывает логику игровых взаимодействий
  - surroundings.py - описание ландшавта карты (builder + singleton + facrory method)
  - WorldObjects.py - описание surroundings, item и characters как объектов игрового мира (decorator)
  - World.py - содержит описание игрового мира 
  - Manager.py - описывает взаимодействие World и gfx