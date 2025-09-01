{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Comma Code\n",
    "\n",
    "spam = ['apples', 'bananas', 'tofu', 'cats']\n",
    "\n",
    "def list_joiner(list):\n",
    "    \"\"\"Take a list and print it as an Oxford comma having sentence.\"\"\"\n",
    "    count = 0\n",
    "    joined = ''\n",
    "    while count < len(list) - 2:\n",
    "        joined += list[count] + ', '\n",
    "        count += 1\n",
    "    joined += list[-2] + ' and '\n",
    "    joined += list[-1] + '.'\n",
    "    return joined\n",
    "    print(joined)\n",
    "        \n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'apples, bananas, tofu and cats.'"
      ]
     },
     "execution_count": 22,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "list_joiner(spam)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Character Picture Grid\n",
    "\n",
    "grid = [['.', '.', '.', '.', '.', '.'],\n",
    "        ['.', 'O', 'O', '.', '.', '.'],\n",
    "        ['O', 'O', 'O', 'O', '.', '.'],\n",
    "        ['O', 'O', 'O', 'O', 'O', '.'],\n",
    "        ['.', 'O', 'O', 'O', 'O', 'O'],\n",
    "        ['O', 'O', 'O', 'O', 'O', '.'],\n",
    "        ['O', 'O', 'O', 'O', '.', '.'],\n",
    "        ['.', 'O', 'O', '.', '.', '.'],\n",
    "        ['.', '.', '.', '.', '.', '.']]\n",
    "\n",
    "for i in range(len(grid[0])):\n",
    "    for j in range(len(grid)):\n",
    "        print(grid[j][i], end='')\n",
    "    print()\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
