from typing import Any


bankcode={
    "ABBANK":"970425",
    "ACB":"970416",
    "AGRIBANK":"970405",
    "BAB":"970409",
    "BIDV":"970488",
    "BVBANK":"970438",
    "COOPBANK":"970446",
    "DABANK":"970406",
    "EXIMBANK":"970431",
    "GPBANK":"970408",
    "HDBANK":"970437",
    "HLBANK":"970442",
    "IVB":"970434",
    "KLB":"970452",
    "LVB":"970449",
    "MB":"970422",
    "MSB":"970426",
    "NAMABANK":"970428",
    "NCB":"970419",
    "OCB":"970448",
    "PGBANK":"970430",
    "PVC":"970412",
    "SCB":"970429",
    "SEA":"970440",
    "SGBANK":"970400",
    "SHINHAN":"970424",
    "SHB":"970443",
    "SACOMBANK":"970403",
    "TECHCOMBANK":"970407",
    "TIENPHONGBANK":"970423",
    "UOB":"970458",
    "VAB":"970427",
    "VC":"970460",
    "VIETCOMBANK":"970436",
    "VCCB":"970454",
    "VIB":"970441",
    "VPBANK":"970432",
    "VRB":"970421",
    "VIETINBANK":"970415",
    "WRB":"970457"
}
def _crc16( data: bytes, last4char = True):
        """
        CRC-16 (CCITT) implemented with a precomputed lookup table
        """
        table = [ 
            0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50A5, 0x60C6, 0x70E7, 0x8108, 0x9129, 0xA14A, 0xB16B, 0xC18C, 0xD1AD, 0xE1CE, 0xF1EF,
            0x1231, 0x0210, 0x3273, 0x2252, 0x52B5, 0x4294, 0x72F7, 0x62D6, 0x9339, 0x8318, 0xB37B, 0xA35A, 0xD3BD, 0xC39C, 0xF3FF, 0xE3DE,
            0x2462, 0x3443, 0x0420, 0x1401, 0x64E6, 0x74C7, 0x44A4, 0x5485, 0xA56A, 0xB54B, 0x8528, 0x9509, 0xE5EE, 0xF5CF, 0xC5AC, 0xD58D,
            0x3653, 0x2672, 0x1611, 0x0630, 0x76D7, 0x66F6, 0x5695, 0x46B4, 0xB75B, 0xA77A, 0x9719, 0x8738, 0xF7DF, 0xE7FE, 0xD79D, 0xC7BC,
            0x48C4, 0x58E5, 0x6886, 0x78A7, 0x0840, 0x1861, 0x2802, 0x3823, 0xC9CC, 0xD9ED, 0xE98E, 0xF9AF, 0x8948, 0x9969, 0xA90A, 0xB92B,
            0x5AF5, 0x4AD4, 0x7AB7, 0x6A96, 0x1A71, 0x0A50, 0x3A33, 0x2A12, 0xDBFD, 0xCBDC, 0xFBBF, 0xEB9E, 0x9B79, 0x8B58, 0xBB3B, 0xAB1A,
            0x6CA6, 0x7C87, 0x4CE4, 0x5CC5, 0x2C22, 0x3C03, 0x0C60, 0x1C41, 0xEDAE, 0xFD8F, 0xCDEC, 0xDDCD, 0xAD2A, 0xBD0B, 0x8D68, 0x9D49,
            0x7E97, 0x6EB6, 0x5ED5, 0x4EF4, 0x3E13, 0x2E32, 0x1E51, 0x0E70, 0xFF9F, 0xEFBE, 0xDFDD, 0xCFFC, 0xBF1B, 0xAF3A, 0x9F59, 0x8F78,
            0x9188, 0x81A9, 0xB1CA, 0xA1EB, 0xD10C, 0xC12D, 0xF14E, 0xE16F, 0x1080, 0x00A1, 0x30C2, 0x20E3, 0x5004, 0x4025, 0x7046, 0x6067,
            0x83B9, 0x9398, 0xA3FB, 0xB3DA, 0xC33D, 0xD31C, 0xE37F, 0xF35E, 0x02B1, 0x1290, 0x22F3, 0x32D2, 0x4235, 0x5214, 0x6277, 0x7256,
            0xB5EA, 0xA5CB, 0x95A8, 0x8589, 0xF56E, 0xE54F, 0xD52C, 0xC50D, 0x34E2, 0x24C3, 0x14A0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405,
            0xA7DB, 0xB7FA, 0x8799, 0x97B8, 0xE75F, 0xF77E, 0xC71D, 0xD73C, 0x26D3, 0x36F2, 0x0691, 0x16B0, 0x6657, 0x7676, 0x4615, 0x5634,
            0xD94C, 0xC96D, 0xF90E, 0xE92F, 0x99C8, 0x89E9, 0xB98A, 0xA9AB, 0x5844, 0x4865, 0x7806, 0x6827, 0x18C0, 0x08E1, 0x3882, 0x28A3,
            0xCB7D, 0xDB5C, 0xEB3F, 0xFB1E, 0x8BF9, 0x9BD8, 0xABBB, 0xBB9A, 0x4A75, 0x5A54, 0x6A37, 0x7A16, 0x0AF1, 0x1AD0, 0x2AB3, 0x3A92,
            0xFD2E, 0xED0F, 0xDD6C, 0xCD4D, 0xBDAA, 0xAD8B, 0x9DE8, 0x8DC9, 0x7C26, 0x6C07, 0x5C64, 0x4C45, 0x3CA2, 0x2C83, 0x1CE0, 0x0CC1,
            0xEF1F, 0xFF3E, 0xCF5D, 0xDF7C, 0xAF9B, 0xBFBA, 0x8FD9, 0x9FF8, 0x6E17, 0x7E36, 0x4E55, 0x5E74, 0x2E93, 0x3EB2, 0x0ED1, 0x1EF0
        ]
        
        crc = 0xFFFF
        for byte in data:
            crc = (crc << 8) ^ table[(crc >> 8) ^ byte]
            crc &= 0xFFFF    # important, crc must stay 16bits all the way through
        if last4char:
            return hex(crc)[-4:].upper() # Get 4 last char and uppercase
        else:
            return hex(crc)

def get_crc16(string = "00020101021238530010A0000007270123000697043201091290057180208QRIBFTTA53037045802VN5920NGUYEN PHAM THUY LAN62390835Thanh toan don hang cho Bean Bakery6304",last4char=True):
        string_byte = bytes(string,"UTF-8")
        return _crc16(data = string_byte, last4char= last4char)
    
def _make_value(code:str,value:str,fix_len=""):
        value = value.replace("/"," ")
        value = value.replace("-"," ")
        if fix_len =="":
            lenvalue = ("0" + str(len(value))) if (len(value) < 10) else str(len(value))
        else:
            lenvalue = fix_len
        result:str = (code + lenvalue + value)
        # print("make value: ---- " , result)
        return result
    
def remove_nonVaccent(input_str:str):
        s1 = u"ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ"
        s0 = u"AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy"
        s = ""
        print (input_str.encode("utf-8"))
        for c in input_str:
            if c in s1:
                s += s0[s1.index(c)]
            else:
                s += c
        return s   


def gen_vietqr_string(acc_no="129005718",acc_holder_name="NGUYEN PHAM THUY LAN",acc_bic="970432",bill_value: str = "", bill_detail:str="",bill_no:str="",qrtype = True, is_bank_acc = True):
    
    """Generate VietQR - Odoo Url

    Keyword arguments:
    argument -- description
        @acc_no             -- The bank account number
        @acc_holder_name    -- The bank account holder name 
        @acc_bic            -- The bank code from Napas
        @is_bank_acc           -- The type of bank account: 'True' value is Bank Account,'False' value is ATM Account
        @bill_value         -- The bill value
        @bill_detail        -- The bill detail information
        @bill_no            -- The bill number
        @height             -- The height of QR image - default:256px
        @width              -- The width of QR image - default:256px
        @qrtype             -- The Type of QR: 'True' value is Dynamic QR,'False' value is Static QR
        
    Return: return_description
        @result -- The VietQR - Odoo Url
        
    Note: List of bank code
        ABBANK:"970425", ACB:"970416", AGRIBANK:"970405", BAB:"970409", BIDV:"970488", BIDV_1:"970418", BVBANK:"970438", 
        COOPBANK:"970446", DABANK:"970406", EXIMBANK:"970431", GPBANK:"970408", HDBANK:"970437", HLBANK:"970442", IVB:"970434", 
        KLB:"970452", LVB:"970449", MB:"970422", MSB:"970426", NAMABANK:"970428", NCB:"970419", OCB:"970448", PGBANK:"970430", 
        PVC:"970412", SCB:"970429", SEA:"970440", SGBANK:"970400", SHINHAN:"970424", SHB:"970443", SACOMBANK:"970403", 
        TECHCOMBANK:"970407", TIENPHONGBANK:"970423", UOB:"970458", VAB:"970427", VC:"970460", VIETCOMBANK:"970436", VCCB:"970454", 
        VIB:"970441", VPBANK:"970432", VRB:"970421", VIENTINBANK:"970415", WRB:"970457",
    """

       
    # define initial value
    init_qrcode:str = "000201010212" if (qrtype == True) else "000201010211"
    napas_account_transfer:str = "0208QRIBFTTA" if ( is_bank_acc == True) else "0208QRIBFTTC"
    billvalue:str = bill_value if (bill_value != "") else "0"
    acc_bic = bankcode.get(acc_bic) if bankcode.get(acc_bic) is not None else acc_bic
    # print(bankcode.get(acc_bic))
    
    # define compute Qrcode
    
    #code 00: Define type of QR   
    napas_id= "0010A000000727"
    #code 38: Define the beneficiary / merchant bank account
    qr_acquirer = _make_value("00",acc_bic)
    qr_merchant_acc = _make_value("01",acc_no )
    qr_beneficiary = _make_value("01",qr_acquirer + qr_merchant_acc + napas_account_transfer,str(len(qr_acquirer) + len(qr_merchant_acc) + len(napas_account_transfer)-12))
    qr_merchant_account_info = _make_value("38",napas_id+qr_beneficiary)
    #code 53: Define currency
    currency_code:str = "5303704"
    #code 54: Define bill value 
    qr_billvalue = _make_value("54",billvalue)
    #code 58: Define country code
    country_code:str = "5802VN"
    #code 59: Defince beneficiary / merchant name
    qr_merchant_name = _make_value("59",acc_holder_name)
    #code 62: define the transaction purpose
    if bill_no !="": 
        qr_purpose = _make_value("08",remove_nonVaccent(bill_detail))
        qr_bill_no = _make_value("01",bill_no+" ")
        qr_purpose = _make_value("62", qr_bill_no + qr_purpose)
    else:
        qr_purpose = _make_value("08",remove_nonVaccent(bill_detail))
        qr_purpose = _make_value("62",qr_purpose)
    #code 63: Define checksum
    crc_begin_code= "6304"  
    #buile Qrcode string
    qrcode = init_qrcode + qr_merchant_account_info + currency_code + qr_billvalue + country_code + qr_merchant_name + qr_purpose + crc_begin_code
    # print(qrcode)
    
    #add Qrcode checksum and return 
    return (qrcode + get_crc16(qrcode,last4char=True))
    
    

def gen_vietqr_url(acc_no="129005718",acc_holder_name="NGUYEN PHAM THUY LAN",acc_bic="970432",bill_value: str = "", bill_detail:str="",bill_no:str="", height:int = 256, width:int=256,qrtype = True, is_bank_acc = True):
    qrcode = gen_vietqr_string(acc_no,acc_holder_name,acc_bic,bill_value, bill_detail,bill_no,qrtype, is_bank_acc)
    result = "/report/barcode/?type=QR&height=%s&width=%s&value=%s" %(height,width,qrcode)
    return result