package demo.survey;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/** A tiny survey, used to show off Java colors. */
public final class Showcase {
    private static final int MAX_ANSWERS = 25;
    private final List<String> answers = new ArrayList<>();

    @Deprecated
    public void legacy() {}

    public Optional<String> add(String text) {
        if (text == null || text.isBlank() || answers.size() >= MAX_ANSWERS) {
            return Optional.empty();
        }
        answers.add(text.trim());
        return Optional.of(text);
    }

    public double average(List<Double> scores) {
        return scores.stream().mapToDouble(Double::doubleValue).average().orElse(0.0);
    }

    public static void main(String[] args) {
        var s = new Showcase();
        s.add("Warm and cozy").ifPresent(System.out::println);
    }
}
