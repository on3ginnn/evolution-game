Evolution game

![](https://github.com/on3ginnn/evolution.gif)

Суть игры
В условиях зараженного космоса нужно сьесть все вражеские "бактерии".

Жаргон
Игок - белый круг с зелынми бортами.
Поинты(очки) - маленькие разноцветные точки, кружки, которые надо съедать.
Мобы(враги) - большой белый круг с красными бортами, его надо избегать.

Правила
-игрок должен поедать микробов (поинтов), тем самым зарабатывать очки.
-игрок должен продержаться до победы, чтобы его не съел враг 
(моб), набрав максимальное количество очков.
-игрок может поедать врагов, если больше их. Если игрок по размеру меньше врага - моб 
съест игрока.
-игрок и мобы могут передвигаться только в пределах поля, ограниченного красными линиями.
-мобы изначально поедают поинты, но если видят игрока на определенном 
расстоянии, и являются больше игрока по размеру, начинают двигаться в сторону игрока.
Если моб меньше игрока - моб будет двигаться в противоположном от игрока напрвалении, 
пока не выйдет из зоны видимости игрока.
-скорость мобов изначательно незначительно меньше, чем скорость игрока (т.к компьютер принимает действия быстрее человека).

Реализованные технологии:
-возможность управлением двумя сторонами одновременно(то есть можно 
зажать UP и LEFT - игрок будет двигаться по диагональному направлению между этими сторонами)
-музыка и звуковые эффекты
-камера привязана над игроком
-масштабирование отображенных объектов при достижении игроком определенных 
размеров(нужно, чтобы размер игрока не был больше размера экрана)
-расчет алгоритма условия съедения
(когда определенная часть тела объекта поглащена другим большим телом 
объекта - большой объект "съедает" маленький, то есть очки маленького объекта 
складываются с очками большого объекта и приписываются большому объекту, 
а маленький объект оказывается "съеденым" - то есть просто исчезает с игрового поля)
-респавн поинтов и мобов после съедения с определенной частотой(то есть на карте 
всегда будут генерироваться поинты(очки для "съедания"), если их количество не удовлетваряет условие. Так же с мобами(врагами).
-расчет алгоритма движения моба к поинтам.
-расчет траектории движения мобов к игроку и от него.
-спрайты обернуты в маску(то есть к примеру, игрок - это круг, и блягодаря маске, фактически он 
является кругом, а не квадратом, стороны которого равны диамерту круга.
-возможность начать игру сначала сразу же после проигрыша или выйгрыша, не перезагружая игру.