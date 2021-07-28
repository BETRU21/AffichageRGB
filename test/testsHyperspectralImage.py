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
		image = HyperSpectralImage()
		self.assertIsNotNone(image)

	def testDefaultDataIsEmpty(self):
		image = HyperSpectralImage()
		self.assertEqual(len(image.data), 0)

	def testDefaultWavelenthIsEmpty(self):
		image = HyperSpectralImage()
		self.assertEqual(len(image.wavelength), 0)

	def testAddWavelength(self):
		image = HyperSpectralImage()
		wavelength = [785, 786, 788, 789]
		image.addWavelength(wavelength)
		equality = np.equal(image.wavelength, np.array([785, 786, 788, 789]))
		result = equality.all()
		self.assertTrue(result)

	def testDeleteWavelength(self):
		image = HyperSpectralImage()
		self.assertEqual(len(image.wavelength), 0)
		wavelength =  [785, 786, 788, 789]
		image.addWavelength(wavelength)
		self.assertEqual(len(image.wavelength), 4)
		image.deleteWavelength()
		self.assertEqual(len(image.wavelength), 0)

	def testReturnWaveNumber(self):
		image = HyperSpectralImage()
		wavelength = [785, 786, 788, 789]
		image.addWavelength(wavelength)
		laserWaveLength = 785
		waveNumber = image.returnWaveNumber(laserWaveLength)
		equality = np.equal(waveNumber, np.array([0., 16., 48., 65.]))
		result = equality.all()
		self.assertTrue(result)

	def testAddSpectrumToData(self):
		image = HyperSpectralImage()
		x = 0
		y = 0
		spectrum = [1, 2, 3, 4]
		image.addSpectrumToData(x, y, spectrum)
		self.assertEqual(len(image.data), 1)
		self.assertEqual(len(image.data[0]), 2)
		self.assertEqual(len(image.data[0][0]), 2)
		self.assertIsInstance(image.data[0][0][0], int)
		self.assertIsInstance(image.data[0][0][1], int)
		self.assertEqual(len(image.data[0][1]), 4)

	def testAdd2SpectraToData(self):
		image = HyperSpectralImage()
		x1 = 15
		y1 = 64
		spectrum1 = [50, -1, 0, 69]

		x2 = 2
		y2 = 3
		spectrum2 = [-550, 10, 6000000, 2]

		image.addSpectrumToData(x1, y1, spectrum1)
		image.addSpectrumToData(x2, y2, spectrum2)
		self.assertEqual(len(image.data), 2)

	@unittest.skipIf(skipTests, "Code not finished")
	def testAdd2SpectraAtTheSameCoords(self):
		image = HyperSpectralImage()
		x1 = 15
		y1 = 64
		spectrum1 = [50, -1, 0, 69]

		x2 = 15
		y2 = 64
		spectrum2 = [-550, 10, 6000000, 2]

		image.addSpectrumToData(x1, y1, spectrum1)
		image.addSpectrumToData(x2, y2, spectrum2)
		self.assertEqual(len(image.data), 2)


	def testDeleteAllSpectrumInData(self):
		image = HyperSpectralImage()
		x = 0
		y = 0
		spectrum = [1, 2, 3, 4]
		image.addSpectrumToData(x, y, spectrum)
		self.assertEqual(len(image.data), 1)
		image.deleteAllSpectrumInData()
		self.assertEqual(len(image.data), 0)



	def testDeleteSpecificSpectrumInDataTrue(self):
		image = HyperSpectralImage()
		x1 = 15
		y1 = 64
		spectrum1 = [50, -1, 0, 69]

		x2 = 14
		y2 = 3
		spectrum2 = [-550, 10, 6000000, 2]

		image.addSpectrumToData(x1, y1, spectrum1)
		image.addSpectrumToData(x2, y2, spectrum2)

		self.assertEqual(len(image.data), 2)
		spectrumFound = image.deleteSpecificSpectrumInData(x1, y1)
		self.assertTrue(spectrumFound)
		self.assertEqual(len(image.data), 1)

	def testDeleteSpecificSpectrumInDataFalse(self):
		image = HyperSpectralImage()
		spectrumFound = image.deleteSpecificSpectrumInData(3, 3)
		self.assertFalse(spectrumFound)

	def testReturnSpectrum(self):
		image = HyperSpectralImage()
		x = 0
		y = 0
		spectrum = [1, 2, 3, 4]
		image.addSpectrumToData(x, y, spectrum)
		returnSpectrum = image.returnSpectrum(x, y, image.data)
		self.assertListEqual(returnSpectrum, spectrum)

	def testReturnSpectrumNone(self):
		image = HyperSpectralImage()
		returnSpectrum = image.returnSpectrum(2, 100, image.data)
		self.assertIsNone(returnSpectrum)

	def testReturnWidthImage(self):
		image = HyperSpectralImage()
		image.addSpectrumToData(0, 0, [1, 2, 3])
		image.addSpectrumToData(0, 1, [4, 5, 6])
		image.addSpectrumToData(1, 0, [7, 8, 9])
		image.addSpectrumToData(1, 1, [10, 11, 12])
		image.addSpectrumToData(2, 0, [13, 14, 15])
		image.addSpectrumToData(2, 1, [16, 17, 18])
		


		width = image.returnWidthImage(image.data)
		self.assertEqual(width, 3)

	def testReturnWidthImageWithNoData(self):
		image = HyperSpectralImage()
		width = image.returnWidthImage(image.data)
		self.assertEqual(width, 0)

	def testReturnHeightImage(self):
		image = HyperSpectralImage()
		image.addSpectrumToData(0, 0, [1, 2, 3])
		image.addSpectrumToData(0, 1, [4, 5, 6])
		image.addSpectrumToData(1, 0, [7, 8, 9])
		image.addSpectrumToData(1, 1, [10, 11, 12])
		image.addSpectrumToData(2, 0, [13, 14, 15])
		image.addSpectrumToData(2, 1, [16, 17, 18])

		width = image.returnHeightImage(image.data)
		self.assertEqual(width, 2)

	def testReturnHeightImageWithNoData(self):
		image = HyperSpectralImage()
		width = image.returnHeightImage(image.data)
		self.assertEqual(width, 0)

	def testReturnSpectrumLen(self):
		image = HyperSpectralImage()
		x = 0
		y = 0
		spectrum = [1, 2, 3, 4]
		image.addSpectrumToData(x, y, spectrum)
		spectrumLen = image.returnSpectrumLen(image.data)

	def testReturnSpectrumLen(self):
		image = HyperSpectralImage()
		spectrumLen = image.returnSpectrumLen(image.data)
		self.assertIsNone(spectrumLen)

	@unittest.skipIf(skipTests, "Code not finished")
	def testReturnSpectrumRange(self):
		image = HyperSpectralImage()
		x = 0
		y = 0
		spectrum = [1, 2, 3, 4]
		image.addSpectrumToData(x, y, spectrum)
		spectrumRange = image.returnSpectrumRange(image.data)
		self.assertEqual()




if __name__ == "__main__":
    unittest.main()