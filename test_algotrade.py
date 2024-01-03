import unittest
import pandas as pd
from algotrade import AlgoTrade  # Replace with the actual module name

class TestAlgoTrade(unittest.TestCase):

    def test_signal_generator_signal_case_0(self):
        # No clear pattern
        test_data = pd.DataFrame({'Open': [10, 20, 30, 40], 'Close': [20, 30, 40, 50]})
        stock = AlgoTrade("AAPL", test_data)
        signal = stock.getSignal()
        self.assertEqual(signal, 0)

    def test_signal_generator_signal_case_1(self):
        # Bearish Pattern
        test_data = pd.DataFrame({'Open': [30, 50], 'Close': [40, 45]})
        stock = AlgoTrade("AAPL", test_data)
        signal = stock.getSignal()
        self.assertEqual(signal, 1)
    
    def test_signal_generator_signal_case_2(self):
        # Bullish Pattern
        test_data = pd.DataFrame({'Open': [40, 30], 'Close': [35, 50]})
        stock = AlgoTrade("AAPL", test_data)
        signal = stock.getSignal()
        self.assertEqual(signal, 2)

if __name__ == '__main__':
    unittest.main()
