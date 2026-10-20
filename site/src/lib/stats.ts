/**
 * MİRAT İstemci Tarafı İstatistiki Hesaplama Motoru
 * Ziyaretçilerin doğrudan tarayıcıda Z-skoru, TOST denklik testi,
 * Bayes faktörü (BF01) ve baz oran karşılaştırması yapmasını sağlar.
 */

// Standart normal dağılım kümülatif dağılım fonksiyonu (CDF)
function normalCDF(z: number): number {
  const b1 = 0.319381530;
  const b2 = -0.356563782;
  const b3 = 1.781477937;
  const b4 = -1.821255978;
  const b5 = 1.330274429;
  const p = 0.2316419;
  const c2 = 0.39894228;

  if (z >= 0.0) {
    const t = 1.0 / (1.0 + p * z);
    return 1.0 - c2 * Math.exp((-z * z) / 2.0) * t * (t * (t * (t * (t * b5 + b4) + b3) + b2) + b1);
  } else {
    const t = 1.0 / (1.0 - p * z);
    return c2 * Math.exp((-z * z) / 2.0) * t * (t * (t * (t * (t * b5 + b4) + b3) + b2) + b1);
  }
}

export interface StatisticalTestResult {
  count1: number;
  count2: number;
  total: number;
  observedProportion: number;
  zScore: number;
  pValue: number;
  isSymmetric: boolean;
  tostEquivalent: boolean;
  tostPValue: number;
  bayesFactorBF01: number;
  bayesInterpretation: string;
  baseRateChance: number;
  scientificVerdict: string;
}

export function computeParityStats(c1: number, c2: number, margin = 0.05): StatisticalTestResult {
  const n = c1 + c2;
  if (n <= 0) {
    return {
      count1: c1,
      count2: c2,
      total: 0,
      observedProportion: 0.5,
      zScore: 0,
      pValue: 1.0,
      isSymmetric: true,
      tostEquivalent: false,
      tostPValue: 1.0,
      bayesFactorBF01: 1.0,
      bayesInterpretation: "Yetersiz Veri",
      baseRateChance: 1.06,
      scientificVerdict: "Yetersiz veri",
    };
  }

  const pObs = c1 / n;
  const se = Math.sqrt(0.25 / n);
  const z = (pObs - 0.5) / se;
  const pVal = 2 * (1 - normalCDF(Math.abs(z)));

  // TOST (Two One-Sided Tests) Equivalence Test
  // H0: |p - 0.5| >= margin vs H1: |p - 0.5| < margin
  const zLower = (pObs - (0.5 - margin)) / se;
  const pLower = 1 - normalCDF(zLower);
  const zUpper = (pObs - (0.5 + margin)) / se;
  const pUpper = normalCDF(zUpper);
  const tostP = Math.max(pLower, pUpper);
  const isEquivalent = tostP < 0.05;

  // Bayes Factor BF01: Point Null (p=0.5) vs Uniform Beta(1,1) Prior
  // Marginal likelihood under H1: 1 / (n + 1)
  // Likelihood under H0: Binomial(k; n, 0.5) = comb(n, k) * 0.5^n
  // BF01 = L(H0) / L(H1) = comb(n, k) * 0.5^n * (n + 1)
  // For numerical stability with large n, use log-gamma:
  function logGamma(x: number): number {
    const cof = [
      76.18009172947146, -86.50532032941677, 24.01409824083091,
      -1.231739572450155, 0.001208650973866179, -0.000005395239384953,
    ];
    let y = x;
    let tmp = x + 5.5;
    tmp -= (x - 0.5) * Math.log(tmp);
    let ser = 1.000000000190015;
    for (let j = 0; j <= 5; j++) {
      ser += cof[j] / ++y;
    }
    return -tmp + Math.log((2.5066282746310005 * ser) / x);
  }

  function logComb(N: number, K: number): number {
    if (K < 0 || K > N) return -Infinity;
    if (K === 0 || K === N) return 0;
    return logGamma(N + 1) - logGamma(K + 1) - logGamma(N - K + 1);
  }

  const logL0 = logComb(n, c1) - n * Math.log(2);
  const logL1 = -Math.log(n + 1);
  const logBF01 = logL0 - logL1;
  const bf01 = Math.min(Math.exp(Math.min(logBF01, 700)), 999999);

  let interpretation = "Yetersiz Kanıt";
  if (bf01 > 100) interpretation = "H0 (Eşitlik) Lehine Ezici (Decisive) Kanıt";
  else if (bf01 > 30) interpretation = "H0 Lehine Çok Güçlü (Very Strong) Kanıt";
  else if (bf01 > 10) interpretation = "H0 Lehine Güçlü (Strong) Kanıt";
  else if (bf01 > 3) interpretation = "H0 Lehine Orta Derece (Moderate) Kanıt";
  else if (bf01 > 1) interpretation = "H0 Lehine Zayıf (Anecdotal) Kanıt";
  else if (bf01 < 0.01) interpretation = "H1 (Farklılık) Lehine Ezici Kanıt";
  else if (bf01 < 0.1) interpretation = "H1 Lehine Güçlü Kanıt";
  else interpretation = "Eşitlik veya Farklılık Yönünde Belirsiz";

  let verdict = "";
  if (c1 === c2 && bf01 > 10) {
    verdict = "ALTIN STANDART: Kusursuz Eşitlik & Güçlü Bayesyen Kanıt";
  } else if (isEquivalent) {
    verdict = "DENK: %5 Marjında İstatistiki Olarak Denk";
  } else if (pVal > 0.05) {
    verdict = "KISMEN DENGELİ: Sıfır Hipotezi Reddedilemedi";
  } else {
    verdict = "ANLAMLI FARK: İki Sayı İstatistiki Olarak Birbirinden Farklı";
  }

  return {
    count1: c1,
    count2: c2,
    total: n,
    observedProportion: Number(pObs.toFixed(4)),
    zScore: Number(z.toFixed(4)),
    pValue: Number(pVal.toFixed(6)),
    isSymmetric: pVal >= 0.05,
    tostEquivalent: isEquivalent,
    tostPValue: Number(tostP.toFixed(4)),
    bayesFactorBF01: Number(bf01.toFixed(2)),
    bayesInterpretation: interpretation,
    baseRateChance: 1.06, // %1.06 corpus baseline for equal roots
    scientificVerdict: verdict,
  };
}

