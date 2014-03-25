t = [12.8, 38.4, 51.2, 64];
can_rel = [1.384E-24, 6.691E-18, 6.862E-13, 4.912E-9];


trend_t = linspace(0, 100);
exp_can = polyfit(t, log(can_rel), 1);
trend_y = exp_can(1)*trend_t + exp_can(2);

o = ones(size(trend_t))(1,:)
flexray_single = o*5.211E-13;
flexray_dual = o*2.716E-25;
flexray_redundant = o*7.374E-50;

plot(t, log(can_rel), 'k');
hold on

plot(trend_t, trend_y, 'o.', trend_t, log(flexray_single), trend_t, log(flexray_dual), trend_t, log(flexray_redundant));

legend("CAN", "CAN Trendline", "FlexRay One Channel", "FlexRay Two Channel", "FlexRay Dual Channel, Dual Message")
ylabel("Probability of System Failure (log scale)");
xlabel("Bus Load (%)");
print -dpng FlexRaySystemReliability.png

