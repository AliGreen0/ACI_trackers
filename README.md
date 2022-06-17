Official implementation of the "Auto-Correct-Integrated trackers with and without memory of first frames" paper.

Link: https://link.springer.com/article/10.1007/s41315-020-00137-0

The main idea behind this tracker is very simple. Suppose there are many trackers tracking an object in a video. If after a number of frames, all trackers produce bounding boxes with similar coordinates except one tracker, that single tracker might have made a mistake and needs correction. This work is based on implementing several trackers and correcting them when they make a mistake.

For more details please refer to the paper.
