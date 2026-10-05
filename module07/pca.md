# 07 Principal Component Analysis

## Big Idea

Principal component analysis (PCA) is an unsupervised method for reducing a large set of variables to a smaller number of synthetic dimensions that preserve as much of the original variation as possible.

This is useful when data are high-dimensional and hard to visualize or model directly. But PCA is not just a black-box procedure for shrinking a table. It is a sequence of decisions about the data, the features, the preprocessing, the retained components, and how the results are interpreted.

A good PCA workflow is not:

**run PCA → keep the first two components → explain the data**

It is:

**question → data/features → preprocessing → PCA → explained variance → component selection → interpretation → sensitivity check → communication**

```{note}
A principal component is not automatically a natural or causal category. It is a mathematical summary of variation in the chosen data representation.
```

## 7.1 Why reduce dimensions?

Many data problems involve dozens, hundreds, or even thousands of variables. In those settings, a table can be difficult to visualize and complex to model.

PCA helps because it can find a smaller set of directions that explain a large share of the variation in the data. This can help with:

- visualization in two or three dimensions
- dimension reduction before clustering or prediction
- summarizing correlated features
- reducing noise and redundancy
- exploring patterns in data with many variables

The key idea is that a dataset often contains correlated variables. If several variables move together, we may be able to summarize their shared variation with a smaller set of component axes.

## 7.2 PCA intuition: finding new directions in the data

A useful way to think about PCA is geometric.

Suppose we have a dataset with two variables, such as sodium and potassium measurements. Instead of looking only at the original axes, PCA rotates the coordinate system to find new directions through the data.

The first principal component, PC1, is the direction along which the projected data have the greatest variance. The second principal component, PC2, is a different direction that is perpendicular to the first one and captures as much of the remaining variation as possible.

This continues for additional components, each one representing another direction in the data. The result is a new coordinate system where the axes are ordered by how much variation they explain.

In a simple expression, each principal component is a weighted linear combination of the original variables:

PC1 = w1x1 + w2x2 + ... + wpxp

The weights are often called **loadings**. They describe how strongly each original variable contributes to that component.

The data points can also be represented in the new component space using **scores**. A score tells us where an observation lies along each principal component.

This is the core difference:

- **scores** describe observations in the new component space
- **loadings** describe how the original variables contribute to each component

## 7.3 Preparing data for PCA

PCA results depend strongly on how the data are prepared. This is one of the most important lessons of the method.

### Centering

PCA is usually applied after centering each variable by subtracting its mean. This changes the origin from zero to the mean of the variable, so the method focuses on variation around the center rather than the arbitrary zero point.

### Scaling

Scaling is especially important when variables are measured on different units or have very different spreads. Without scaling, a variable with a large numerical range can dominate the component calculation simply because its values are large in magnitude.

This is why standardization is often used:

- subtract the mean
- divide by the standard deviation

That gives each variable a roughly comparable scale.

This is not always the best choice in every setting. Sometimes the original scale itself contains meaningful information. If variables are already on a common and meaningful measurement scale, forcing standardization may hide important structure. PCA is therefore sensitive to feature scale and to the analyst’s choices about preprocessing.

### Transformations and feature choices

Other decisions also matter:

- whether to apply a log transformation to skewed data
- how to handle outliers
- which variables to include in the analysis
- whether to aggregate or subset features before running PCA

These choices can change the components and the interpretation. That is not a bug in PCA. It is an important reminder that the method is not discovering a unique objective truth in the raw data alone; it is summarizing a chosen representation of the data.

```{note}
A PCA result is only as trustworthy as the feature set and preprocessing decisions behind it.
```

## 7.4 Scores, loadings, and explained variance

Once PCA is computed, we look at two main outputs: scores and loadings.

### Scores

Scores are the coordinates of observations in the PCA space. If an observation has a high score on a component, it is located far along that component direction.

Scores are useful for:

- plotting observations in a reduced space
- identifying clusters or gradients
- comparing cases in a lower-dimensional representation

### Loadings

Loadings are the weights of the original variables in each component. They reveal which variables contribute most strongly to a component.

If a component has large positive loadings for a set of variables, those variables tend to move together in the same direction. Large negative loadings indicate the opposite direction. The size of the loading indicates strength; the sign indicates direction.

The sign itself is not inherently meaningful. If we multiply all loadings in a component by -1, the component direction flips, but the underlying structure is the same. The important idea is the pattern of relative magnitudes and directions.

```{warning}
Large loadings do not automatically mean a variable is a true cause or a natural category. They mean the variable contributes strongly to the mathematical variation captured by that component.
```

### Variance explained

Each principal component explains some share of the variation in the original data. A component with high explained variance captures a large amount of the information in the dataset.

The total variation retained by the first K components can be summarized with:

- **proportion of variance explained** for each component
- **cumulative explained variance** across components

This helps show how much information remains after reducing dimensionality.

## 7.5 Choosing how many components to keep

One of the hardest questions in PCA is deciding how many components to retain.

A common tool is the **scree plot**, which shows the proportion of variance explained against the component number. The “elbow” is a useful visual cue: the curve drops sharply at first and then flattens.

This is a helpful heuristic, but it is not a universal rule. The right number of components depends on the purpose of the analysis.

For example:

- for visualization, a small number of components may be enough
- for compression, a moderate number may be needed
- for downstream modeling, a different threshold may be preferred
- for interpretation, fewer components may be easier to explain

A scree plot is evidence, not proof. It should be used alongside domain understanding, model goals, and sensitivity checks.

## 7.6 Interpreting and visualizing PCA results

PCA is often used to make high-dimensional data easier to understand visually or descriptively. But a component is only interpretable after we inspect it.

A responsible interpretation asks:

- Which variables have the largest loadings?
- Do the loadings make sense in the context of the problem?
- Do the score plots show meaningful groups, gradients, or outliers?
- Does the apparent structure persist under reasonable alternative choices?
- Is the interpretation plausible for a domain expert?

This is where PCA becomes an applied statistical tool rather than a purely mechanical one.

It is also where caution matters. A component might look meaningful because it captures a lot of variance, but that does not mean it represents a hidden real-world construct, a latent cause, or a natural category. The component is still a mathematical summary of the selected data representation.

## 7.7 Sensitivity and responsible use

One of the strongest applied lessons in PCA is that defensible modeling choices can change the output.

A few common examples:

- standardizing versus not standardizing
- including or excluding a feature
- applying a log transformation to skewed variables
- handling outliers differently
- keeping a different number of components

These decisions can produce different loadings, scores, and visual patterns. That does not make PCA unreliable. It means PCA is part of a reasoning process, not a single objective truth generated automatically from raw numbers.

This is why we should check whether a PCA interpretation is reasonably stable under defensible alternative choices. If the structure disappears when we change preprocessing, we should be careful about claiming strong conclusions.

```{note}
The goal is not to find a magical “true” PCA. The goal is to understand whether the result is interpretable, useful, and reasonably stable.
```

## 7.8 What PCA can and cannot tell us

PCA is powerful, but it has important limits.

### What PCA does well

- captures linear directions of variation
- summarizes redundant variables
- helps visualize high-dimensional data
- supports clustering, compression, and modeling workflows
- reduces complexity while preserving much of the signal

### What PCA does not do

- it does not use a target variable
- it does not establish causality
- it does not guarantee semantic meaning for the components
- it is sensitive to preprocessing choices and feature selection
- it prioritizes variance, not necessarily task relevance
- it is limited to linear structure

This is why a high explained variance does not automatically mean a component is useful for every downstream task. A PCA summary may be mathematically strong but not operationally meaningful.

## Key Takeaways

- PCA is a method for finding directions of maximum variation in data.
- The first component captures the largest variance, and later components capture remaining orthogonal variation.
- Scores describe observations in the reduced space; loadings describe how original variables contribute to each component.
- Preprocessing is central: centering, scaling, transformations, and feature selection can change the result.
- Scree plots and variance explained are useful tools, but they are not automatic decision rules.
- PCA is interpretable only when we inspect loadings, score plots, and domain context.
- Component interpretation requires caution: PCA does not automatically reveal hidden real-world categories or causal structure.

# References

- Yu, B., & Barter, R. *Veridical Data Science*. Chapter 6: Principal Component Analysis. https://vdsbook.com/06-pca
- Yu, B., & Barter, R. *Veridical Data Science*. Book website.
