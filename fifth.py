from manim import *

class DeriveEquationsOfMotion(Scene):
    def construct(self):
        title = Text("Derivation of Equations of Motion via Integration", font_size=30).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Step 1: a = dv/dt
        step1 = MathTex(r"a = \frac{dv}{dt}", color=YELLOW).scale(1.1).to_edge(LEFT, buff=1).shift(UP*2)
        step1_explain = Text("Acceleration is rate of change of velocity", font_size=20, color=WHITE).next_to(step1, DOWN, buff=0.2)
        
        self.play(Write(step1))
        self.play(Write(step1_explain))
        self.wait(1)

        # Step 2: dv = a dt
        step2 = MathTex(r"dv = a \, dt", color=GREEN).scale(1.1).next_to(step1, DOWN, buff=1)
        arrow1 = Arrow(step1.get_bottom(), step2.get_top(), color=WHITE, buff=0.1, stroke_width=3)
        multiply = Text("Multiply both sides by dt", font_size=18, color=GRAY).next_to(arrow1, RIGHT, buff=0.2)

        self.play(Create(arrow1), Write(multiply), Write(step2))
        self.wait(1)

        # Step 3: Integrate
        step3 = VGroup(
            MathTex(r"\int_{v_0}^{v} dv = \int_{0}^{t} a \, dt", color=BLUE).scale(1.0),
            MathTex(r"[v]_{v_0}^{v} = a [t]_{0}^{t} \quad (\text{a constant})", color=BLUE).scale(0.9),
        ).arrange(DOWN, buff=0.3).next_to(step2, DOWN, buff=0.8)

        self.play(Write(step3[0]))
        self.wait(0.8)
        self.play(Write(step3[1]))
        self.wait(1)

        # Step 4: v = v0 + at
        step4 = MathTex(r"v - v_0 = a t", r"\quad \Rightarrow \quad", r"v = v_0 + a t", color=YELLOW).scale(1.0)
        step4.next_to(step3, DOWN, buff=0.8)
        box4 = SurroundingRectangle(step4, color=YELLOW, buff=0.2)

        self.play(Write(step4), Create(box4))
        self.wait(1.5)

        self.play(FadeOut(step1), FadeOut(step1_explain), FadeOut(arrow1), FadeOut(multiply), FadeOut(step2), FadeOut(step3))
        self.play(step4.animate.to_edge(UP, buff=1.5).shift(LEFT*0.5), FadeOut(box4), FadeOut(title))
        self.wait(0.5)

        # Step 5: v = dx/dt
        step5 = MathTex(r"v = \frac{dx}{dt}", color=ORANGE).scale(1.1).to_edge(LEFT, buff=1).shift(UP*0.5)
        step5_explain = Text("Velocity is rate of change of displacement", font_size=20).next_to(step5, DOWN, buff=0.2)

        self.play(Write(step5), Write(step5_explain))
        self.wait(1)

        step6 = MathTex(r"dx = v \, dt = (v_0 + a t) dt", color=GREEN).scale(1.0).next_to(step5, DOWN, buff=0.8)
        self.play(Write(step6))
        self.wait(1)

        step7 = VGroup(
            MathTex(r"\int_{x_0}^{x} dx = \int_{0}^{t} (v_0 + a t) dt", color=BLUE).scale(0.95),
            MathTex(r"x - x_0 = v_0 t + \frac{1}{2} a t^2", color=BLUE).scale(0.95),
        ).arrange(DOWN, buff=0.3).next_to(step6, DOWN, buff=0.8)

        self.play(Write(step7[0]))
        self.wait(0.8)
        self.play(Write(step7[1]))
        self.wait(1)

        step8 = MathTex(r"x = x_0 + v_0 t + \frac{1}{2} a t^2", color=YELLOW).scale(1.1).next_to(step7, DOWN, buff=0.8)
        box8 = SurroundingRectangle(step8, color=YELLOW, buff=0.2)

        self.play(Write(step8), Create(box8))
        self.wait(2)

        # Clear for incline application
        self.play(FadeOut(step4), FadeOut(step5), FadeOut(step5_explain), FadeOut(step6), FadeOut(step7), FadeOut(step8), FadeOut(box8))

        # Apply to incline
        incline_title = Text("Apply to Inclined Plane:", font_size=28, color=BLUE).to_edge(UP, buff=0.5)
        self.play(Write(incline_title))

        incline_eqs = VGroup(
            MathTex(r"a = g(\sin\theta - \mu_k \cos\theta)", color=WHITE).scale(0.9),
            MathTex(r"\Downarrow", color=GRAY).scale(0.8),
            MathTex(r"v(t) = v_0 + g(\sin\theta - \mu_k \cos\theta) t", color=ORANGE).scale(0.85),
            MathTex(r"s(t) = s_0 + v_0 t + \frac{1}{2} g(\sin\theta - \mu_k \cos\theta) t^2", color=GREEN).scale(0.8),
            MathTex(r"\text{If } v_0=0, s_0=0: \quad s = \frac{1}{2} g(\sin\theta - \mu_k \cos\theta) t^2", color=YELLOW).scale(0.75),
        ).arrange(DOWN, buff=0.4).center().shift(DOWN*0.2)

        for eq in incline_eqs:
            self.play(Write(eq), run_time=1)
            self.wait(0.5)

        self.wait(2)
