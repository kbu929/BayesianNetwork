import unittest
import numpy as np
import bayesnet as bn


class TestMultivariateGaussian(unittest.TestCase):

    def test_multivariate_gaussian(self):
        self.assertRaises(ValueError, bn.random.MultivariateGaussian, np.zeros(2), np.eye(3))
        self.assertRaises(ValueError, bn.random.MultivariateGaussian, np.zeros(2), np.eye(2) * -1)

        x_train = np.array([
            [1., 1.],
            [1., -1],
            [-1., 1.],
            [-1., -2.]
        ])
        mu = bn.Parameter(np.ones(2))
        cov = bn.Parameter(np.eye(2) * 2)
        optimizer = bn.optimizer.GradientDescent([mu, cov], 0.1)
        for _ in range(1000):
            optimizer.cleargrad()
            x = bn.random.MultivariateGaussian(mu, cov + cov.transpose(), data=x_train)
            loss = -x.log_pdf().sum()
            loss.backward()
            optimizer.update()
        self.assertTrue(np.allclose(mu.value, x_train.mean(axis=0)))
        self.assertTrue(np.allclose(np.cov(x_train, rowvar=False, bias=True), x.cov.value))

        g = bn.random.MultivariateGaussian(
            np.ones(2), np.eye(2) * 2
        )
        self.assertEqual(g.KLqp(g).value, 0)


if __name__ == '__main__':
    unittest.main()