#wrong last layer act
#wrong loss input
#increasing widths
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD
import numpy


X = numpy.array([[1., 1.], [0., 0.], [1., 0.], [0., 1.], [1., 1.], [0., 0.]])
y = numpy.array([[0.], [0.], [1.], [1.], [0.], [0.]])
model = Sequential()
model.add(Dense(2, input_dim=2, init='uniform', activation='sigmoid'))
model.add(Dense(3, init='uniform', activation='sigmoid'))
#softmax cannot be used for 1-D vector
model.add(Dense(1, init='uniform', activation='softmax'))
sgd = SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='mean_squared_error', optimizer=sgd)

model.fit(X, y, nb_epoch=20)
print()
score = model.evaluate(X, y)
print()
print(score)
print(model.predict(numpy.array([[1, 0]])))
print(model.predict(numpy.array([[0, 0]])))