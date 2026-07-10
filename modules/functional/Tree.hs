module Types where

import Data.List (sort, minimumBy, maximumBy)
import Data.Function (on)
import qualified Data.Map.Strict as Map

type Feature = Double
type Sample = [Feature]
type Observation a = (Sample, a)
type Dataset a = [Observation a]

numSamples :: Dataset a -> Int
numSamples = length

labels :: Dataset a -> [a]
labels = map snd

samples :: Dataset a -> [Sample]
samples = map fst

numClasses :: Eq a => Dataset a -> Int
numClasses = length
    . unique
    . labels
    

data Tree a
    = Leaf a
    | Node
        Int -- index
        Double -- threshold
        (Tree a) -- left branch
        (Tree a) -- right branch
    deriving Show


predict :: Tree a -> Sample -> a
predict (Leaf label) _ = label
predict (Node index threshold left right) sample =
    let feature = sample !! index
    in if feature <= threshold
        then predict left sample
        else predict right sample
    
frequency :: Eq a => [a] -> [(a, Int)]
frequency [] = []
frequency (x:xs) =
    (x, count x (x:xs)) : frequency (filter (/= x) xs)

count :: Eq a => a -> [a] -> Int
count x = length . filter (== x)

unique :: Eq a => [a] -> [a]
unique [] = []
unique (x:xs) = x : unique (filter (/= x) xs)

probabilities :: Eq a => Dataset a -> [Double]
probabilities dataset =
    let total = fromIntegral (length dataset)
        freqs = frequency (labels dataset)
    in map (\(_, count) -> fromIntegral count / total) freqs

gini :: Eq a => Dataset a -> Double
gini =
    (1 -)
    . sum
    . map (^ (2::Int))
    . probabilities

data Split = Split 
    { featureIndex :: Int
    , threshold    :: Double
    }
    deriving Show

data CandidateSplit = CandidateSplit
    { split :: Split
    , impurity :: Double
    }
    deriving Show

partitionDataset :: Split -> Dataset a -> (Dataset a, Dataset a)
partitionDataset split dataset = (left, right)
    where
        left = filter goesLeft dataset
        right = filter (not . goesLeft) dataset
        goesLeft (sample, _) = sample !! featureIndex split <= threshold split

splitGini :: Eq a => Split -> Dataset a -> Double
splitGini split dataset =
    leftWeight * gini left + rightWeight * gini right
    where
        (left, right) = partitionDataset split dataset
        total = fromIntegral (length dataset)
        leftWeight = fromIntegral (length left) / total
        rightWeight = fromIntegral (length right) / total

featureColumn :: Int -> Dataset a -> [Double]
featureColumn index = map (\(sample, _) -> sample !! index)

candidateThresholds :: Int -> Dataset a -> [Double]
candidateThresholds index dataset =
    map midpoint pairs
    where
        values = unique $ sort $ featureColumn index dataset
        pairs = zip values (tail values)
        midpoint (a, b) = (a + b) / 2

numFeatures :: Dataset a -> Int
numFeatures [] = 0
numFeatures ((sample, _):_) = length sample

allSplits :: Dataset a -> [Split]
allSplits dataset =
    concatMap splitsForFeature [0 .. numFeatures dataset - 1]
    where
        splitsForFeature feature =
            map
                (\threshold -> Split feature threshold)
                (candidateThresholds feature dataset)

bestSplit :: Eq a => Dataset a -> Maybe Split
bestSplit dataset =
    case validSplits of
        [] -> Nothing
        splits -> Just $ minimumBy compareSplit splits
    where
        compareSplit = compare `on` (\split -> splitGini split dataset)

frequencyMap :: Ord a => Dataset a -> Map.Map a Int
frequencyMap = foldr insert Map.empty
    where
        insert (_, label) = Map.insertWith (+) label 1


majorityLabel :: Ord a => Dataset a -> Maybe a
majorityLabel dataset
    | Map.null table = Nothing
    | otherwise = Just $ fst $ maximumBy (compare `on` snd) (Map.toList table)
    where
        table = frequencyMap dataset

pureNode :: Eq a => Dataset a -> Bool
pureNode [] = True
pureNode ((_, label):xs) = all ((== label) . snd) xs

validSplit :: Split -> Dataset a -> Bool
validSplit split dataset =
    not (null left) && not (null right)
    where
        (left, right) = partitionDataset split dataset

validSplits = filter (\s -> validSplit s dataset) (allSplits dataset)

trainTree :: (Eq a,Ord a) => Int -> Dataset a -> Maybe (Tree a)
trainTree _ [] = Nothing
trainTree depth ((_,label):xs)
    | all ((== label) . snd) xs = Just (Leaf label)
    | depth <= 0 = Leaf <$> majorityLabel ((_,label):xs)
    | otherwise = do
        split <- bestSplit dataset
        let (left,right) = partitionDataset split dataset
        leftTree <- trainTree (depth-1) left
        rightTree <- trainTree (depth-1) right
        return $ Node (featureIndex split) (threshold split) leftTree rightTree

dataset :: Dataset Int
dataset =
    [ ([150],0)
    , ([155],0)
    , ([160],0)
    , ([170],1)
    , ([175],1)
    , ([180],1)
    ]

main = do
    let tree = trainTree 5 dataset
    print tree