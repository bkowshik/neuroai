# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import pytest
import torch

from .augmentations import (
    BandstopFilterFFT,
    FTSurrogateConfig,
    SignFlipConfig,
    TrivialBrainAugment,
    TrivialBrainAugmentConfig,
)


@pytest.mark.parametrize("sfreq", [100, 250])
@pytest.mark.parametrize("bandwidth", [2, 4])
def test_bandstop_filter_fft(sfreq, bandwidth):
    transform = BandstopFilterFFT(sfreq=sfreq, bandwidth=bandwidth)
    x = torch.randn(10, 2, 512)
    z = transform(x)
    # Only check shape for now
    assert z.shape == x.shape


@pytest.mark.parametrize("sfreq", [100, 250])
def test_trivial_brain_augment(sfreq):
    transform = TrivialBrainAugment(TrivialBrainAugmentConfig(sfreq=sfreq))
    x = torch.randn(10, 2, 512)
    z = transform(x)
    # Only check shape for now
    assert z.shape == x.shape


@pytest.mark.parametrize("probability,expected_sign", [(0.0, 1.0), (1.0, -1.0)])
def test_sign_flip_config(probability, expected_sign):
    transform = SignFlipConfig(probability=probability).build()
    x = torch.randn(10, 2, 512)
    z = transform(x)
    assert z.shape == x.shape
    # probability=1 flips every example's sign; probability=0 leaves it unchanged
    assert torch.allclose(z, expected_sign * x)


@pytest.mark.parametrize("channel_indep", [False, True])
@pytest.mark.parametrize("phase_noise_magnitude", [0.5, 1.0])
def test_ft_surrogate_config(phase_noise_magnitude, channel_indep):
    transform = FTSurrogateConfig(
        probability=1.0,
        phase_noise_magnitude=phase_noise_magnitude,
        channel_indep=channel_indep,
    ).build()
    x = torch.randn(10, 2, 512)
    z = transform(x)
    # Phase randomization preserves shape; values are stochastic
    assert z.shape == x.shape
