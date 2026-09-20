# 05 Decision Trees, Random Forests, and Factor Analysis

## Big Idea

This week is about two different ways to look for structure in data:

- **decision trees** and **random forests** for prediction
- **factor analysis** for finding hidden patterns in many related variables

The main skill is not just knowing the names. It is knowing when a method is useful, what it tells you, and what it does not tell you.

## 5.1 Why tree-based models matter

Tree-based models are useful when you want a model that is easy to follow and can handle non-linear patterns. They are often appealing because they break a problem into a series of simple questions.

Trees are popular for two reasons:

- they can be easy to explain
- they can fit patterns that a straight line would miss

That flexibility is helpful, but it also creates risk. A tree that is too complex can fit noise instead of signal.

## 5.2 How a decision tree predicts

A decision tree works by splitting the data again and again using yes/no questions.

- The top of the tree is the **root**.
- Each question creates smaller groups.
- The final group is a **leaf**.
- The leaf gives the prediction.

For a classification problem, the leaf may predict a class or a probability. For a regression problem, the leaf usually predicts an average value.

## 5.3 Complexity and overfitting

Simple trees are easy to read, but they may miss important structure. Very deep trees can fit the training data too closely.

That is the basic tradeoff:

- **too simple**: the model misses real patterns
- **too complex**: the model learns noise and generalizes poorly

This is why tree depth and other stopping rules matter. They help control overfitting.

## 5.4 Why random forests help

A single tree can change a lot if the data change a little. Random forests reduce that instability by combining many trees.

They usually work by:

- training each tree on a bootstrap sample of the data
- letting each split consider only a random subset of features
- averaging the trees together

The result is usually more stable and more accurate than a single tree. But the forest is harder to explain in a simple picture.

Feature importance can help show which variables matter most, but it should be read carefully. Importance is not the same as causation.

## 5.5 A brief factor analysis summary

Factor analysis is used when many observed variables seem to reflect a smaller number of hidden ideas or traits.

Think of it this way:

- **observed variables** are the measurements you have
- **latent factors** are the hidden patterns you infer

Two key terms are useful here:

- **factor loadings**: how strongly a variable relates to a factor
- **communality**: how much of a variable is shared with the factors

Factor analysis is not the same as PCA. PCA is mostly about compression and variance. Factor analysis is about explaining shared structure.

## 5.6 What to remember

- Trees are easy to follow, but deeper trees can overfit.
- Random forests improve stability by averaging many trees.
- Feature importance is useful, but it is not a causal explanation.
- Factor analysis looks for hidden structure in correlated variables.
- Factor analysis and PCA answer different questions.

## References

- Yu, B., & Barter, R. *Veridical Data Science*. Chapter 12: Decision Trees and the Random Forest Algorithm.
- Hair, J. F., Black, W. C., Babin, B. J., & Anderson, R. E. *Multivariate Data Analysis* (factor analysis section used in the course packet).
