#ifndef HELP_CLASSES_H
#define HELP_CLASSES_H
class IR {
private:
  byte m_pin;
  int maxWhiteValue=45;
public:
  void set_pin(byte pin);
  bool IsWhite();
  bool IsBlack();
  void printIR(char Name);
};
#endif
