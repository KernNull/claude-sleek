<?php
declare(strict_types=1);

namespace Demo\Survey;

use InvalidArgumentException;

/** A tiny survey, used to show off PHP colors. */
final class Survey
{
    private const MAX = 25;
    private array $answers = [];

    public function __construct(private string $title, public readonly bool $anonymous = true) {}

    public function add(string $text, ?float $score = null): static
    {
        if (trim($text) === '' || count($this->answers) >= self::MAX) {
            throw new InvalidArgumentException("Bad answer for {$this->title}");
        }
        $this->answers[] = ['text' => $text, 'score' => $score];
        return $this;
    }

    public function average(): float
    {
        $scores = array_filter(array_column($this->answers, 'score'));
        return $scores ? array_sum($scores) / count($scores) : 0.0;
    }
}

echo (new Survey('Favorite theme'))->add('Warm', 0.9)->average(), PHP_EOL;
