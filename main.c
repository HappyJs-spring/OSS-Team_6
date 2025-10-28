#include <stdio.h>

double add(double a, double b) {
    return a + b;
}

//빼기
double subtract(double a, double b) {
    return a - b;
}

double multiply(double a, double b) {
    return a * b;
}

double Remainder(double a, double b) {
    if ((int)b == 0) {
        printf("0으로 나눌 수 없습니다.\n");
        return 0;
    }
    return (double)((int)a % (int)b);
}

int main() {
    double x, y;
    int choice;

    printf("===== 팀 계산기 =====\n");
    printf("1. 더하기\n");
    printf("2. 빼기\n");
    printf("3. 곱하기\n");
    printf("4. 나눗셈\n");
    printf("5. 나머지\n");
    printf("선택: ");
    scanf_s("%d", &choice);

    printf("첫 번째 숫자 입력: ");
    scanf_s("%lf", &x);
    printf("두 번째 숫자 입력: ");
    scanf_s("%lf", &y);

    switch (choice) {
    case 1:
        printf("결과: %.2lf\n", add(x, y));
        break;
    case 2:
        printf("결과: %.2lf\n", subtract(x, y));
        break;
    case 3:
        printf("결과: %.2lf\n", multiply(x, y));
        break;
    case 4:
        printf("결과: %.2lf\n", divide(x, y));
        break;
    case 5:
        printf("결과(나머지): %.0lf\n", Remainder(x, y));
        break;
    default:
        printf("잘못된 선택입니다.\n");
    }

    return 0;
}
