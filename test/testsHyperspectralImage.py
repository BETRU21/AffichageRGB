import unittest
import sys
import os
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.HyperSpectralImage import HyperSpectralImage

# HSI = HyperSpectralImage

skipTests = True

class TestHyperSpectralImage(unittest.TestCase):

	def testImportHSI(self):
		self.assertIsNotNone(HyperSpectralImage)

	def testCreateHSIInstance(self):
		HSI = HyperSpectralImage(False)
		self.assertIsNotNone(HSI)

	def testDefaultDataIsEmpty(self):
		HSI = HyperSpectralImage()
		self.assertEqual(len(HSI.data), 0)

	def testDefaultWavelenthIsEmpty(self):
		HSI = HyperSpectralImage()
		self.assertEqual(len(HSI.wavelength), 0)

	def testAddWavelength(self):
		HSI = HyperSpectralImage()
		wavelength = [785, 786, 788, 789]
		HSI.addWavelength(wavelength)
		equality = np.equal(HSI.wavelength, np.array([785, 786, 788, 789]))
		result = equality.all()
		self.assertTrue(result)

	def testDeleteWavelength(self):
		HSI = HyperSpectralImage()
		self.assertEqual(len(HSI.wavelength), 0)
		wavelength =  [785, 786, 788, 789]
		HSI.addWavelength(wavelength)
		self.assertEqual(len(HSI.wavelength), 4)
		HSI.deleteWavelength()
		self.assertEqual(len(HSI.wavelength), 0)

	def testReturnWaveNumber(self):
		HSI = HyperSpectralImage()
		wavelength = [785, 786, 788, 789]
		HSI.addWavelength(wavelength)
		laserWaveLength = 785
		waveNumber = HSI.returnWaveNumber(laserWaveLength)
		equality = np.equal(waveNumber, np.array([0., 16., 48., 65.]))
		result = equality.all()
		self.assertTrue(result)

	def testAddSpectrumToData(self):
		HSI = HyperSpectralImage()
		x = 0
		y = 0
		spectrum = [1, 2, 3, 4]
		HSI.addSpectrumToData(x, y, spectrum)
		self.assertEqual(len(HSI.data), 1)
		self.assertEqual(len(HSI.data[0]), 3)
		self.assertIsInstance(HSI.data[0].x, int)
		self.assertIsInstance(HSI.data[0].y, int)
		self.assertEqual(len(HSI.data[0].spectrum), 4)

	def testAdd2SpectraToData(self):
		HSI = HyperSpectralImage()
		x1 = 15
		y1 = 64
		spectrum1 = [50, -1, 0, 69]

		x2 = 2
		y2 = 3
		spectrum2 = [-550, 10, 6000000, 2]

		HSI.addSpectrumToData(x1, y1, spectrum1)
		HSI.addSpectrumToData(x2, y2, spectrum2)
		self.assertEqual(len(HSI.data), 2)

	@unittest.skipIf(skipTests, "Code not finished")
	def testAdd2SpectraAtTheSameCoords(self):
		HSI = HyperSpectralImage()
		x1 = 15
		y1 = 64
		spectrum1 = [50, -1, 0, 69]

		x2 = 15
		y2 = 64
		spectrum2 = [-550, 10, 6000000, 2]

		HSI.addSpectrumToData(x1, y1, spectrum1)
		HSI.addSpectrumToData(x2, y2, spectrum2)
		self.assertEqual(len(HSI.data), 2)

	def testDeleteAllSpectrumInData(self):
		HSI = HyperSpectralImage()
		x = 0
		y = 0
		spectrum = [1, 2, 3, 4]
		HSI.addSpectrumToData(x, y, spectrum)
		self.assertEqual(len(HSI.data), 1)
		HSI.deleteAllSpectrumInData()
		self.assertEqual(len(HSI.data), 0)

	def testReturnSpectrum(self):
		HSI = HyperSpectralImage()
		x = 0
		y = 0
		spectrum = [1, 2, 3, 4]
		HSI.addSpectrumToData(x, y, spectrum)
		returnSpectrum = HSI.returnSpectrum(x, y, HSI.data)
		self.assertListEqual(returnSpectrum, spectrum)

	def testReturnSpectrumNone(self):
		HSI = HyperSpectralImage()
		returnSpectrum = HSI.returnSpectrum(2, 100, HSI.data)
		self.assertIsNone(returnSpectrum)

	def testReturnWidthImage(self):
		HSI = HyperSpectralImage()
		HSI.addSpectrumToData(0, 0, [1, 2, 3])
		HSI.addSpectrumToData(0, 1, [4, 5, 6])
		HSI.addSpectrumToData(1, 0, [7, 8, 9])
		HSI.addSpectrumToData(1, 1, [10, 11, 12])
		HSI.addSpectrumToData(2, 0, [13, 14, 15])
		HSI.addSpectrumToData(2, 1, [16, 17, 18])

		width = HSI.returnWidthImage(HSI.data)
		self.assertEqual(width, 3)

	def testReturnWidthImageWithNoData(self):
		HSI = HyperSpectralImage()
		width = HSI.returnWidthImage(HSI.data)
		self.assertEqual(width, 0)

	def testReturnHeightImage(self):
		HSI = HyperSpectralImage()
		HSI.addSpectrumToData(0, 0, [1, 2, 3])
		HSI.addSpectrumToData(0, 1, [4, 5, 6])
		HSI.addSpectrumToData(1, 0, [7, 8, 9])
		HSI.addSpectrumToData(1, 1, [10, 11, 12])
		HSI.addSpectrumToData(2, 0, [13, 14, 15])
		HSI.addSpectrumToData(2, 1, [16, 17, 18])

		width = HSI.returnHeightImage(HSI.data)
		self.assertEqual(width, 2)

	def testReturnHeightImageWithNoData(self):
		HSI = HyperSpectralImage()
		width = HSI.returnHeightImage(HSI.data)
		self.assertEqual(width, 0)

	def testReturnSpectrumLen(self):
		HSI = HyperSpectralImage()
		x = 0
		y = 0
		spectrum = [1, 2, 3, 4]
		HSI.addSpectrumToData(x, y, spectrum)
		spectrumLen = HSI.returnSpectrumLen(HSI.data)

	def testReturnSpectrumLen(self):
		HSI = HyperSpectralImage()
		spectrumLen = HSI.returnSpectrumLen(HSI.data)
		self.assertIsNone(spectrumLen)

	def testReturnSpectrumRange(self):
		HSI = HyperSpectralImage()
		wavelength = [785, 786, 788, 789]
		HSI.addWavelength(wavelength)
		spectrumRange = HSI.returnSpectrumRange(HSI.wavelength)
		self.assertEqual(spectrumRange, 4)

	def testReturnSpectrumRangeNone(self):
		HSI = HyperSpectralImage()
		spectrumRange = HSI.returnSpectrumRange(HSI.wavelength)
		self.assertIsNone(spectrumRange)

	def testDataToMatrix(self):
		HSI = HyperSpectralImage()
		HSI.addSpectrumToData(0, 0, [1, 2, 3])
		HSI.addSpectrumToData(0, 1, [4, 5, 6])
		HSI.addSpectrumToData(1, 0, [7, 8, 9])
		HSI.addSpectrumToData(1, 1, [10, 11, 12])
		HSI.addSpectrumToData(2, 0, [13, 14, 15])
		HSI.addSpectrumToData(2, 1, [16, 17, 18])

		testMatrix = np.zeros((2, 3, 3))
		testMatrix[0][0] = np.array([1, 2, 3])
		testMatrix[1][0] = np.array([4, 5, 6])
		testMatrix[0][1] = np.array([7, 8, 9])
		testMatrix[1][1] = np.array([10, 11, 12])
		testMatrix[0][2] = np.array([13, 14, 15])
		testMatrix[1][2] = np.array([16, 17, 18])

		matrix = HSI.dataToMatrix(HSI.data)
		equality = np.equal(matrix, testMatrix)
		result = equality.all()
		self.assertTrue(result)

	def testDataToMatrixNoData(self):
		HSI = HyperSpectralImage()
		matrix = HSI.dataToMatrix(HSI.data)
		self.assertIsNone(matrix)

	def testDataToRGB(self):
		HSI = HyperSpectralImage()
		HSI.addSpectrumToData(0, 0, [1, 2, 3, 4, 5, 6])
		HSI.addSpectrumToData(0, 1, [7, 8, 9, 10, 11, 12])
		HSI.addSpectrumToData(1, 0, [13, 14, 15, 16, 17, 18])
		HSI.addSpectrumToData(1, 1, [19, 20, 21, 22, 23, 24])
		matrix = HSI.dataToRGB(HSI.data, [0, 85, 86, 170, 171, 255])

		testMatrix = np.zeros((2, 2, 3))
		testMatrix[0][0] = np.array([3, 7, 11])
		testMatrix[1][0] = np.array([15, 19, 23])
		testMatrix[0][1] = np.array([27, 31, 35])
		testMatrix[1][1] = np.array([39, 43, 47])
		testMatrix = (testMatrix / np.max(testMatrix)) * 255
		testMatrix = testMatrix.round(0)

		equality = np.equal(matrix, testMatrix)
		result = equality.all()
		self.assertTrue(result)

	def testDataToRGBGlobalMaximumFalse(self):
		HSI = HyperSpectralImage()
		HSI.addSpectrumToData(0, 0, [1, 2, 3, 4, 5, 6])
		HSI.addSpectrumToData(0, 1, [7, 8, 9, 10, 11, 12])
		HSI.addSpectrumToData(1, 0, [13, 14, 15, 16, 17, 18])
		HSI.addSpectrumToData(1, 1, [19, 20, 21, 22, 23, 24])

		testMatrix = np.zeros((2, 2, 3))
		testMatrix[0][0] = np.array([3, 7, 11])
		testMatrix[1][0] = np.array([15, 19, 23])
		testMatrix[0][1] = np.array([27, 31, 35])
		testMatrix[1][1] = np.array([39, 43, 47])
		maxima = testMatrix.max(axis=2)
		maxima = np.dstack((maxima,) * 3)
		testMatrix /= maxima
		testMatrix *= 255
		testMatrix = testMatrix.round(0)

		matrix = HSI.dataToRGB(HSI.data, [0, 85, 86, 170, 171, 255], globalMaximum=False)
		equality = np.equal(matrix, testMatrix)
		result = equality.all()
		self.assertTrue(result)

	def testDataToRGBNoData(self):
		HSI = HyperSpectralImage()
		matrix = HSI.dataToRGB(HSI.data, [0, 85, 86, 170, 171, 255])
		self.assertIsNone(matrix)

if __name__ == "__main__":
    unittest.main()