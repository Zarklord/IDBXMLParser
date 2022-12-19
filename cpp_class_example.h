
class PrimaryBaseClass
{
    uint32_t baseMemberVariable;
    void baseMemberFunction(uint8_t arg1);
    virtual uint16_t baseVirtualFunction();
}

class SecondaryBaseClass
{
    uint16_t secondaryMemberVariable;
    uint8_t secondaryMemberFunction(uint16_t arguement);
    virtual void secondaryVirtualFunction(bool arg1, bool arg2);
}

class DerivedClass : public PrimaryBaseClass, public SecondaryBaseClass
{
    char secondaryMemberVariable;
    uint8_t derivedMemberFunction(uint16_t arguement);
    virtual uint32_t derivedVirtualFunction();
    virtual uint16_t baseVirtualFunction();
}