# Applied-Machine-learning-Project---Fall-2014
#####'Assorter-rectifier' classifier which is pipe lining of high-bias &amp; low-variance classifier build as part of Applied Machine learning class in Fall 2014.
  

    This project is an implementation of the proposal by Cheuk Ting LI from Stanford, in his project - An Ensemble Classifier for 
    Rectifying Classification Error. The main idea is to use ensemble methods to combine multiple classifiers in which each constituent 
    classifier would focus on correcting errors made by the previous one. In our case we consider two constituent classifiers - an 
    assorter and a rectifier. The first classifier, the assorter, would perform classification on the training set by generating a 
    probability distribution of the class labels for each example and ranking them accordingly i.e. the label with the highest 
    probability would be ranked 1 and so on. The subsequent classifier, or the rectifier, would use the rank as the class label to 
    perform classification. The rectifier would then learn from the training set and decide if the prediction of the assorter could be 
    used or of it would have to pick from the other classes determined as less likely by the assorter. To classify a test instance, run 
    the assorter to obtain a ranking and pick the class label predicted by the rectifier. Intuitively, using ensemble methods such as a 
    bagging and boosting on a high bias classifier as the assorter followed by a high variance classifier as the rectifier would enhance 
    performance.

##### Please find the REPORT.pdf for more details
