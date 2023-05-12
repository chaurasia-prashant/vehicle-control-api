"""models added to db

Revision ID: 612909954caa
Revises: 
Create Date: 2023-05-07 19:32:41.367862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '612909954caa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Email_Verification',
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('otp', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('email')
    )
    op.create_index(op.f('ix_Email_Verification_email'), 'Email_Verification', ['email'], unique=False)
    op.create_table('accounts',
    sa.Column('empId', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(length=600), nullable=True),
    sa.Column('department', sa.String(), nullable=True),
    sa.Column('phoneNumber', sa.String(), nullable=True),
    sa.Column('isAuthorized', sa.Boolean(), nullable=True),
    sa.Column('verifyPhoneNumber', sa.Boolean(), nullable=True),
    sa.Column('verifyEmail', sa.Boolean(), nullable=True),
    sa.Column('isOwner', sa.String(), nullable=True),
    sa.Column('isAdmin', sa.Boolean(), nullable=True),
    sa.Column('uid', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('empId')
    )
    op.create_index(op.f('ix_accounts_empId'), 'accounts', ['empId'], unique=True)
    op.create_table('booking_backup',
    sa.Column('bookingMonth', sa.String(), nullable=False),
    sa.Column('bookedTime', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('bookingMonth')
    )
    op.create_index(op.f('ix_booking_backup_bookingMonth'), 'booking_backup', ['bookingMonth'], unique=False)
    op.create_table('employeeId',
    sa.Column('empId', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('empId')
    )
    op.create_index(op.f('ix_employeeId_empId'), 'employeeId', ['empId'], unique=True)
    op.create_table('vehicle_Bookings',
    sa.Column('bookingNumber', sa.String(), nullable=False),
    sa.Column('empId', sa.String(), nullable=True),
    sa.Column('empUsername', sa.String(), nullable=True),
    sa.Column('userDepartment', sa.String(), nullable=True),
    sa.Column('isGuestBooking', sa.Boolean(), nullable=True),
    sa.Column('guestName', sa.String(), nullable=True),
    sa.Column('guestMobileNumber', sa.String(), nullable=True),
    sa.Column('vehicleType', sa.String(), nullable=True),
    sa.Column('tripDate', sa.String(), nullable=True),
    sa.Column('startLocation', sa.String(), nullable=True),
    sa.Column('destination', sa.String(), nullable=True),
    sa.Column('startTime', sa.String(), nullable=True),
    sa.Column('endTime', sa.String(), nullable=True),
    sa.Column('vehicleAlloted', sa.String(), nullable=True),
    sa.Column('vehicleNumber', sa.String(), nullable=True),
    sa.Column('tripStatus', sa.Boolean(), nullable=True),
    sa.Column('tripCompleted', sa.Boolean(), nullable=True),
    sa.Column('tripCanceled', sa.Boolean(), nullable=True),
    sa.Column('reason', sa.String(), nullable=True),
    sa.Column('remark', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('bookingNumber')
    )
    op.create_index(op.f('ix_vehicle_Bookings_bookingNumber'), 'vehicle_Bookings', ['bookingNumber'], unique=False)
    op.create_table('vehicle_Details',
    sa.Column('vehicleNumber', sa.String(), nullable=False),
    sa.Column('vehiclePhoneNumber', sa.String(), nullable=True),
    sa.Column('vehicleType', sa.String(), nullable=True),
    sa.Column('bookedTime', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('vehicleNumber')
    )
    op.create_index(op.f('ix_vehicle_Details_vehicleNumber'), 'vehicle_Details', ['vehicleNumber'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_vehicle_Details_vehicleNumber'), table_name='vehicle_Details')
    op.drop_table('vehicle_Details')
    op.drop_index(op.f('ix_vehicle_Bookings_bookingNumber'), table_name='vehicle_Bookings')
    op.drop_table('vehicle_Bookings')
    op.drop_index(op.f('ix_employeeId_empId'), table_name='employeeId')
    op.drop_table('employeeId')
    op.drop_index(op.f('ix_booking_backup_bookingMonth'), table_name='booking_backup')
    op.drop_table('booking_backup')
    op.drop_index(op.f('ix_accounts_empId'), table_name='accounts')
    op.drop_table('accounts')
    op.drop_index(op.f('ix_Email_Verification_email'), table_name='Email_Verification')
    op.drop_table('Email_Verification')
    # ### end Alembic commands ###