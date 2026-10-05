t = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)"
print(t.split("[image](https://i.imgur.com/zjjcJKZ.png)", 1))
