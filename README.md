# Wordbase-Hack
A simple(not really) script to hack into [wordbase](https://play.google.com/store/apps/details?id=com.wordbaseapp) android game.

## How does it work?

###### In short:
* It takes up a screenshot image of the game along with your color(i.e. Blue or Orange) and provides you with possible words you can play. Also, you can choose to show only those words which intersects with the opposite color(with a cost of few extra seconds)

###### In not-so-short:
* ##### Creating training images
  * `create_image` from `pre-process.py` takes an image(screenshot) and breaks it up into 13*10 pieces containing individual letters and save them to a folder called `train_images` after resizing each of them to 19x16 followed by performing some thresholding stuffs.
* ##### Training the model
  * Take each image from `train_images` folder and associate corresponding labels to them(Labels are just respective alphabet letters).
  * Reshape(to 1D) and normalize(0 to 255 => 0 to 1) the image array.
  * Finally, train the model upon reshaped-array using `LinearSVC` method from `sklearn.svm` and save the model with the name `svm_model` in the root directory.
* ##### Generating letter grid
  * `get_grid` from `pre-process.py` uses the above trained model to produce an exact grid(2D-array) of letters from a given screenshot along with lists containing positions of blue and orange tiles.
* ##### Finally, getting words
  * Finally, `solve` from `main.py` uses the grid to filter out possible words starting from position of given-colour tiles.
  * It uses a list of English words, which is stored as a list in `word_list.py`, to compare for possible words.
  * Why not use `word_list.txt` directly rather than saving it in a `.py` file and then using the `.py` file? Because importing `.py` file will create a `.pyc` file upon first execution of the script which will be used in further execution thereby cutting down the execution time almost by a factor of 10.
  * For depth understanding of word-generation, consider reading the [codebase](https://github.com/shashi278/wordbase-hack/blob/master/src/main.py) :)
